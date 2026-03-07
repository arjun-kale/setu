"""Scheme discovery API: GET /api/schemes, GET /api/schemes/{id}. Data from PostgreSQL."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query

from app.config.database import get_db_session
from app.models.scheme import Scheme
from app.models.schemas import EligibilityRuleOut, SchemeListResponse, SchemeOut
from app.services.scheme_service import search_schemes
from sqlalchemy.orm import Session, joinedload

router = APIRouter()


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


@router.get("", response_model=SchemeListResponse)
def list_schemes(
    db: Session = Depends(get_db_session),
    q: Optional[str] = Query(None, description="Search by keyword in name, description, benefits"),
) -> SchemeListResponse:
    """List schemes. Use ?q=farmer to search by keyword."""
    schemes = search_schemes(db, query=q, limit=50)
    return SchemeListResponse(schemes=schemes)


@router.get("/{scheme_id}", response_model=SchemeOut)
def get_scheme(scheme_id: int, db: Session = Depends(get_db_session)) -> SchemeOut:
    """Get one scheme by id with eligibility rules."""
    scheme = (
        db.query(Scheme)
        .options(joinedload(Scheme.eligibility))
        .filter(Scheme.id == scheme_id)
        .first()
    )
    if not scheme:
        raise HTTPException(status_code=404, detail="Scheme not found")
    return _scheme_to_out(scheme)
