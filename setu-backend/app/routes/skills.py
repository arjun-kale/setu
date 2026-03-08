"""Skill learning API: GET /api/skills, GET /api/skills/{id}."""

from fastapi import APIRouter, HTTPException

from app.services.skill_service import get_skill, list_skills

router = APIRouter()


@router.get("/skills")
def list_skills_endpoint():
    """List all learning topics."""
    return {"skills": list_skills()}


@router.get("/skills/{skill_id}")
def get_skill_endpoint(skill_id: str):
    """Get one skill by id."""
    skill = get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return skill
