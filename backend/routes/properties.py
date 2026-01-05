from flask import Blueprint, request, jsonify
from sqlalchemy import or_

from models import Property
from db import SessionLocal  # or db.session if you use Flask-SQLAlchemy

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
    print("HIT /properties")
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