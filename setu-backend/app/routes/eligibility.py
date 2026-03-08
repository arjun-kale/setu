"""Eligibility check API: POST /api/check-eligibility. Query scheme_eligibility, return matching schemes."""

from fastapi import APIRouter, Depends

from app.config.database import get_db_session
from app.models.schemas import CheckEligibilityRequest, CheckEligibilityResponse
from app.services.eligibility_service import check_eligibility
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("", response_model=CheckEligibilityResponse)
def check_eligibility_endpoint(
    body: CheckEligibilityRequest,
    db: Session = Depends(get_db_session),
) -> CheckEligibilityResponse:
    """Check eligibility: query scheme_eligibility and return schemes matching age, income, state, occupation."""
    schemes = check_eligibility(
        db,
        age=body.age,
        income=body.income,
        state=body.state,
        occupation=body.occupation,
    )
    return CheckEligibilityResponse(schemes=schemes)
