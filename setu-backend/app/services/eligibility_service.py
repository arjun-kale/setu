"""Eligibility check logic. Used by API and chat flow."""

import re
from typing import Optional

from sqlalchemy.orm import Session, joinedload

from app.models.scheme import Scheme, SchemeEligibility
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


def _parse_age_range(s: str) -> tuple[int | None, int | None]:
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
        return (int(m.group(1)), int(m.group(1)))
    return (None, None)


def _parse_income_max(s: str) -> float | None:
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
        occ_lower = occupation.strip().lower()
        row_occ_lower = row.occupation.strip().lower()
        if row_occ_lower not in occ_lower and occ_lower not in row_occ_lower:
            return False
    return True


def check_eligibility(
    db: Session,
    *,
    age: Optional[int] = None,
    income: Optional[float] = None,
    state: Optional[str] = None,
    occupation: Optional[str] = None,
) -> list[SchemeOut]:
    """Return schemes matching the given profile. Empty if no profile data."""
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
            if _eligibility_row_matches(row, age, income, state, occupation):
                matching.append(_scheme_to_out(scheme))
                break
    return matching
