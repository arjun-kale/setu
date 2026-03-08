"""Scheme search and eligibility logic. Used by APIs and chat flow."""

from typing import Optional

from sqlalchemy import or_
from sqlalchemy.orm import Session, joinedload

from app.models.scheme import Scheme
from app.models.schemas import EligibilityRuleOut, SchemeOut


def _scheme_to_out(scheme: Scheme) -> SchemeOut:
    rules = [
        EligibilityRuleOut(
            age_limit=getattr(e, "age_limit", None),
            income_limit=getattr(e, "income_limit", None),
            state=getattr(e, "state", None),
            occupation=getattr(e, "occupation", None),
        )
        for e in (scheme.eligibility or [])
    ]
    return SchemeOut(
        id=scheme.id,
        name=scheme.name,
        description=scheme.description,
        benefits=scheme.benefits,
        eligibility_rules=rules,
    )


def search_schemes(db: Session, query: Optional[str] = None, limit: int = 10) -> list[SchemeOut]:
    """
    Search schemes by keyword in name, description, benefits.
    If query is empty/None, return all schemes (up to limit).
    """
    q = (
        db.query(Scheme)
        .options(joinedload(Scheme.eligibility))
        .order_by(Scheme.id)
    )
    if query and query.strip():
        term = f"%{query.strip().lower()}%"
        q = q.filter(
            or_(
                Scheme.name.ilike(term),
                Scheme.description.ilike(term),
                Scheme.benefits.ilike(term),
            )
        )
    schemes = q.limit(limit).all()
    return [_scheme_to_out(s) for s in schemes]


def get_all_schemes(db: Session) -> list[SchemeOut]:
    """Get all schemes with eligibility rules."""
    schemes = (
        db.query(Scheme)
        .options(joinedload(Scheme.eligibility))
        .order_by(Scheme.id)
        .all()
    )
    return [_scheme_to_out(s) for s in schemes]
