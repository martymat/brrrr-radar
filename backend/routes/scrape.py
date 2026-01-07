from datetime import datetime, timezone
from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError

from db import SessionLocal
from models import Property, ScrapeRun
from scraper.mock_scraper import run_mock_scrape  # you can swap later

scrape_bp = Blueprint("scrape", __name__)

@scrape_bp.post("/scrape/run")
def run_scrape():
    payload = request.get_json(silent=True) or {}

    query = (payload.get("query") or "").strip()
    max_results = payload.get("max_results")

    # ---- validate input ----
    if not query:
        return jsonify({"error": "'query' is required"}), 400

    try:
        max_results = int(max_results)
    except (TypeError, ValueError):
        return jsonify({"error": "'max_results' must be an integer"}), 400

    if max_results < 1 or max_results > 200:
        return jsonify({"error": "'max_results' must be between 1 and 200"}), 400

    session = SessionLocal()
    run = None
    try:
        # ---- create scrape_runs row ----
        run = ScrapeRun(
            query=query,
            status="started",
            properties_found=0,
            error_count=0,
            error_samples=None,
        )
        session.add(run)
        session.commit()  # get run.id

        inserted = 0
        skipped = 0
        errors = 0
        error_samples = []

        # ---- run scraper synchronously ----
        scraped_items = run_mock_scrape(query=query, max_results=max_results)

        # ---- ingest into properties (skip duplicates by listing_url) ----
        for item in scraped_items:
            try:
                exists = (
                    session.query(Property.id)
                    .filter(Property.listing_url == item["listing_url"])
                    .first()
                )
                if exists:
                    skipped += 1
                    continue

                session.add(Property(**item))
                session.flush()  # forces insert now (catches unique violation)
                inserted += 1

            except IntegrityError:
                session.rollback()
                skipped += 1
            except Exception as e:
                session.rollback()
                errors += 1
                if len(error_samples) < 10:
                    error_samples.append({"listing_url": item.get("listing_url"), "error": str(e)})

        session.commit()

        # ---- update run record with counts + status ----
        run.properties_found = len(scraped_items)
        run.error_count = errors
        run.error_samples = error_samples if error_samples else None
        run.finished_at = datetime.now(timezone.utc)
        run.status = "succeeded" if errors == 0 else "succeeded_with_errors"
        session.commit()

        # ---- return summary ----
        return jsonify({
            "run_id": run.id,
            "status": run.status,
            "query": query,
            "max_results": max_results,
            "properties_found": len(scraped_items),
            "inserted_count": inserted,
            "skipped_count": skipped,
            "error_count": errors,
        })

    except Exception as e:
        session.rollback()
        # best-effort mark run failed
        try:
            if run and run.id:
                run.status = "failed"
                run.finished_at = datetime.now(timezone.utc)
                run.error_count = (run.error_count or 0) + 1
                run.error_samples = (run.error_samples or []) + [{"error": str(e)}]
                session.commit()
        except Exception:
            session.rollback()

        return jsonify({"error": "Scrape run failed", "details": str(e)}), 500
    finally:
        session.close()

@scrape_bp.get("/scrape/runs")
def list_scrape_runs():
    session = SessionLocal()
    try:
        runs = (
            session.query(ScrapeRun)
            .order_by(ScrapeRun.started_at.desc())
            .limit(50)
            .all()
        )

        return jsonify({
            "items": [
                {
                    "id": r.id,
                    "query": r.query,
                    "max_results": getattr(r, "max_results", None),
                    "status": r.status,
                    "started_at": r.started_at.isoformat() if r.started_at else None,
                    "finished_at": r.finished_at.isoformat() if r.finished_at else None,
                    "properties_found": r.properties_found,
                    "error_count": r.error_count,
                }
                for r in runs
            ]
        })
    finally:
        session.close()

@scrape_bp.get("/scrape/runs/<int:run_id>")
def get_scrape_run(run_id: int):
    session = SessionLocal()
    try:
        r = session.query(ScrapeRun).filter(ScrapeRun.id == run_id).one_or_none()
        if r is None:
            return jsonify({"error": f"ScrapeRun {run_id} not found"}), 404

        return jsonify({
            "id": r.id,
            "query": r.query,
            "max_results": getattr(r, "max_results", None),
            "status": r.status,
            "started_at": r.started_at.isoformat() if r.started_at else None,
            "finished_at": r.finished_at.isoformat() if r.finished_at else None,
            "properties_found": r.properties_found,
            "error_count": r.error_count,
            "error_samples": r.error_samples,
        })
    finally:
        session.close()