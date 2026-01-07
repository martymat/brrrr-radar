from flask import Blueprint, request, jsonify
from sqlalchemy import or_
from sqlalchemy.orm import selectinload

from models import Property, AnalysisResult
from db import SessionLocal
from decimal import Decimal

properties_bp = Blueprint("properties", __name__)

def _get_int(name: str, default: int, *, min_value=None, max_value=None):
    raw = request.args.get(name)
    if raw is None or raw == "":
        value = default
    else:
        try:
            value = int(raw)
        except ValueError:
            raise ValueError(f"'{name}' must be an integer")

    if min_value is not None and value < min_value:
        value = min_value
    if max_value is not None and value > max_value:
        value = max_value
    return value

def _get_float(name: str):
    raw = request.args.get(name)
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except ValueError:
        raise ValueError(f"'{name}' must be a number")

@properties_bp.get("/properties")
def get_properties():
    try:
        page = _get_int("page", 1, min_value=1)
        page_size = _get_int("page_size", 20, min_value=1, max_value=100)

        q = (request.args.get("q") or "").strip()
        min_price = _get_float("min_price")
        max_price = _get_float("max_price")
        min_beds = _get_int("min_beds", 0, min_value=0)
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    session = SessionLocal()
    try:
        query = session.query(Property)

        if q:
            like = f"%{q}%"
            query = query.filter(
                or_(
                    Property.address.ilike(like),
                    Property.city.ilike(like),
                    Property.state.ilike(like),
                    Property.zip.ilike(like),
                )
            )

        if min_price is not None:
            query = query.filter(Property.price >= min_price)

        if max_price is not None:
            query = query.filter(Property.price <= max_price)

        if min_beds > 0:
            query = query.filter(Property.beds >= min_beds)

        total = query.count()

        items = (
            query.order_by(Property.created_at.desc())
                 .offset((page - 1) * page_size)
                 .limit(page_size)
                 .all()
        )

        return jsonify({
            "items": [p.to_dict() for p in items],
            "total": total,
            "page": page,
            "page_size": page_size,
        })
    finally:
        session.close()

@properties_bp.get("/properties/<int:property_id>")
def get_property(property_id: int):
    session = SessionLocal()
    try:
        prop = (
            session.query(Property)
            .options(selectinload(Property.photos))
            .filter(Property.id == property_id)
            .one_or_none()
        )

        if prop is None:
            return jsonify({"error": f"Property {property_id} not found"}), 404

        analysis = (
            session.query(AnalysisResult)
            .filter(AnalysisResult.property_id == property_id)
            .one_or_none()
        )

        return jsonify({
            **prop.to_dict(),
            "photos": [p.to_dict() for p in (prop.photos or [])],
            "analysis": analysis.to_dict() if analysis else None,
        })
    
    finally:
        session.close()

@properties_bp.post("/properties/<int:property_id>/analyze")
def analyze_property(property_id: int):
    session = SessionLocal()
    try:
        prop = session.query(Property).filter(Property.id == property_id).one_or_none()
        if prop is None:
            return jsonify({"error": f"Property {property_id} not found"}), 404

        score_total, score_breakdown, reasons = compute_analysis(prop)

        analysis = (
            session.query(AnalysisResult)
            .filter(AnalysisResult.property_id == property_id)
            .one_or_none()
        )

        if analysis is None:
            analysis = AnalysisResult(
                property_id=property_id,
                score_total=Decimal(str(score_total)),
                score_breakdown=score_breakdown,
                reasons=reasons,
            )
            session.add(analysis)
        else:
            analysis.score_total = Decimal(str(score_total))
            analysis.score_breakdown = score_breakdown
            analysis.reasons = reasons
            analysis.analyzed_at = func.now()
            analysis.updated_at = func.now()

        session.commit()
        session.refresh(analysis)

        return jsonify(analysis.to_dict())
    except Exception as e:
        session.rollback()
        return jsonify({"error": "Analyze failed", "details": str(e)}), 500
    finally:
        session.close()


def compute_analysis(prop: Property):
    # Baseline metrics (purely from property fields for now)
    price = float(prop.price) if prop.price is not None else None
    beds = prop.beds
    sqft = prop.sqft

    desc = (prop.description or "").lower()
    rehab_per_sqft = 35 if any(w in desc for w in ["fixer", "rehab", "needs", "tlc"]) else 20
    rehab_estimate = (sqft * rehab_per_sqft) if sqft else (price * 0.08 if price else None)

    arv_estimate = ((price + rehab_estimate) * 1.10) if (price and rehab_estimate) else None
    rent_estimate = max(1200, (beds or 0) * 650 + (sqft or 0) * 0.40) if (beds or sqft) else None

    # Ratios
    rent_to_price = ((rent_estimate * 12) / price) if (rent_estimate and price) else None
    arv_to_price = (arv_estimate / price) if (arv_estimate and price) else None

    # Score components (0-100 total, simple heuristic)
    score = 0.0
    reasons = []

    if rent_to_price is not None:
        # 0.20 annual rent/price ~= strong
        score += min(45.0, rent_to_price * 150.0)
        reasons.append(f"Rent-to-price ratio: {rent_to_price:.3f}")

    if arv_to_price is not None:
        score += min(35.0, max(0.0, (arv_to_price - 1.0) * 140.0))
        reasons.append(f"ARV-to-price ratio: {arv_to_price:.3f}")

    if beds is not None:
        score += min(10.0, beds * 2.0)
        reasons.append(f"Bedrooms: {beds}")

    # Penalties for missing data
    if price is None:
        score -= 15.0
        reasons.append("Missing price")
    if sqft is None:
        score -= 5.0
        reasons.append("Missing sqft")

    score = max(0.0, min(100.0, score))

    score_breakdown = {
        "price": price,
        "beds": beds,
        "sqft": sqft,
        "rehab_estimate": rehab_estimate,
        "arv_estimate": arv_estimate,
        "rent_estimate": rent_estimate,
        "rent_to_price": rent_to_price,
        "arv_to_price": arv_to_price,
    }

    return score, score_breakdown, reasons
