"""Eligibility check API: POST /api/check-eligibility. Query scheme_eligibility, return matching schemes."""

import re

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, joinedload

from app.config.database import get_db_session
from app.models.scheme import Scheme, SchemeEligibility
from app.models.schemas import (
    CheckEligibilityRequest,
    CheckEligibilityResponse,
    EligibilityRuleOut,
    SchemeOut,
)

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


def _parse_age_range(s: str) -> tuple[int | None, int | None]:
    """Parse age_limit string to (min, max). E.g. '18-60' -> (18, 60), '21+' -> (21, None)."""
    if not s or not s.strip():
        return (None, None)
    s = s.strip()
    if "-" in s:
        m = re.match(r"(\d+)\s*-\s*(\d+)", s)
        if m:
            return (int(m.group(1)), int(m.group(2)))
    if "+" in s or "+" in s.replace(" ", ""):
        m = re.search(r"(\d+)\s*\+", s)
        if m:
            return (int(m.group(1)), None)
    m = re.search(r"(\d+)", s)
    if m:
        n = int(m.group(1))
        return (n, n)
    return (None, None)


def _parse_income_max(s: str) -> float | None:
    """Parse income_limit to max value. E.g. '2 lakh' -> 200000, '50000' -> 50000."""
    if not s or not s.strip():
        return None
    s = s.strip().lower().replace(",", "")
    m = re.search(r"([\d.]+)\s*lakh", s)
    if m:
        return float(m.group(1)) * 100_000
    m = re.search(r"([\d.]+)", s)
    if m:
        return float(m.group(1))
    return None


def _eligibility_row_matches(
    row: SchemeEligibility,
    age: int | None,
    income: float | None,
    state: str | None,
    occupation: str | None,
) -> bool:
    """Return True if user (age, income, state, occupation) matches this eligibility row."""
    if age is not None and row.age_limit:
        lo, hi = _parse_age_range(row.age_limit)
        if lo is not None and age < lo:
            return False
        if hi is not None and age > hi:
            return False
    if income is not None and row.income_limit:
        max_inc = _parse_income_max(row.income_limit)
        if max_inc is not None and income > max_inc:
            return False
    if state and row.state:
        if row.state.strip().lower() != state.strip().lower():
            return False
    if occupation and row.occupation:
        if row.occupation.strip().lower() not in occupation.strip().lower() and occupation.strip().lower() not in row.occupation.strip().lower():
            return False
    return True


@router.post("", response_model=CheckEligibilityResponse)
def check_eligibility(
    body: CheckEligibilityRequest,
    db: Session = Depends(get_db_session),
) -> CheckEligibilityResponse:
    """Check eligibility: query scheme_eligibility and return schemes matching age, income, state, occupation."""
    schemes = (
        db.query(Scheme)
        .options(joinedload(Scheme.eligibility))
        .order_by(Scheme.id)
        .all()
    )
    matching: list[SchemeOut] = []
    for scheme in schemes:
        if not scheme.eligibility:
            continue
        for row in scheme.eligibility:
            if _eligibility_row_matches(
                row,
                body.age,
                body.income,
                body.state,
                body.occupation,
            ):
                matching.append(_scheme_to_out(scheme))
                break
    return CheckEligibilityResponse(schemes=matching)
