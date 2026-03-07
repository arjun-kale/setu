"""User profile API: PUT /api/users/{user_id}/profile — set profile for eligibility check in chat."""

from fastapi import APIRouter, Depends

from app.models.schemas import UpdateProfileRequest
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service

router = APIRouter()


@router.put("/users/{user_id}/profile")
def update_profile(
    user_id: str,
    body: UpdateProfileRequest,
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
):
    """
    Update user profile (age, income, state, occupation).
    Used for eligibility check in chat when user asks "am I eligible?".
    """
    profile = body.model_dump(exclude_none=True)
    if not profile:
        return {"message": "No profile data provided", "user_id": user_id}
    dynamo.update_user_profile(user_id, **profile)
    return {"message": "Profile updated", "user_id": user_id}
