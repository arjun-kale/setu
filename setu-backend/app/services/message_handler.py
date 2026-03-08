"""Unified message handler: intent detection + routing to scheme search, eligibility, or chat."""

from typing import Any, Optional

from sqlalchemy.orm import Session

from app.services.ai_agent import get_ai_response
from app.services.dynamodb_service import DynamoDBService
from app.services.eligibility_service import check_eligibility
from app.services.intent_detection import detect_intent
from app.services.scheme_service import search_schemes
from app.services.skill_service import format_skills_for_chat, get_skill


def _format_schemes_response(schemes: list) -> str:
    """Format scheme list as readable text."""
    if not schemes:
        return "No schemes found matching your search."
    lines = []
    for i, s in enumerate(schemes[:5], 1):
        name = getattr(s, "name", s.get("name", "?"))
        desc = getattr(s, "description", s.get("description", "")) or ""
        desc_short = (desc[:100] + "...") if len(desc) > 100 else desc
        lines.append(f"{i}. **{name}**\n   {desc_short}")
    if len(schemes) > 5:
        lines.append(f"... and {len(schemes) - 5} more. Use GET /api/schemes to see all.")
    return "\n\n".join(lines)


def _format_eligibility_response(schemes: list) -> str:
    """Format eligible schemes as readable text."""
    if not schemes:
        return "Based on your profile, no schemes match your eligibility. You can try the eligibility form with different details."
    lines = [f"You may be eligible for {len(schemes)} scheme(s):"]
    for i, s in enumerate(schemes[:5], 1):
        name = getattr(s, "name", s.get("name", "?"))
        lines.append(f"{i}. {name}")
    if len(schemes) > 5:
        lines.append(f"... and {len(schemes) - 5} more.")
    return "\n".join(lines)


def _parse_profile(profile: Optional[dict[str, Any]]) -> tuple[Optional[int], Optional[float], Optional[str], Optional[str]]:
    """Extract age, income, state, occupation from user profile."""
    if not profile:
        return (None, None, None, None)
    age = profile.get("age")
    if age is not None:
        try:
            age = int(float(age))
        except (ValueError, TypeError):
            age = None
    income = profile.get("income")
    if income is not None:
        try:
            income = float(income)  # Handles int, float, Decimal, str
        except (ValueError, TypeError):
            income = None
    state = profile.get("state") or profile.get("state_code")
    if state and isinstance(state, str):
        state = state.strip() or None
    occupation = profile.get("occupation")
    if occupation and isinstance(occupation, str):
        occupation = occupation.strip() or None
    return (age, income, state, occupation)


def process_message(
    message: str,
    *,
    user_id: str,
    session_id: str,
    language: str,
    dynamo: DynamoDBService,
    db: Session,
    chat_history: Optional[list[dict[str, Any]]] = None,
) -> str:
    """
    Process user message: detect intent, route to scheme search / eligibility / chat.
    Returns the response text.
    """
    intent = detect_intent(message)

    if intent == "scheme_search":
        schemes = search_schemes(db, query=message, limit=10)
        return _format_schemes_response(schemes)

    if intent == "eligibility_check":
        profile = dynamo.get_user_profile(user_id)
        age, income, state, occupation = _parse_profile(profile)
        if age is None and income is None and not state and not occupation:
            return (
                "To check your eligibility, please provide your age, income, state, and occupation. "
                "You can use the eligibility form or tell me: e.g. 'I am 25, farmer from Maharashtra, income 1.5 lakh'."
            )
        schemes = check_eligibility(db, age=age, income=income, state=state, occupation=occupation)
        return _format_eligibility_response(schemes)

    if intent == "skill_learning":
        # Check if user asked about a specific topic
        text_lower = message.strip().lower()
        if any(kw in text_lower for kw in ["banking", "upi", "digital payment", "pay"]):
            skill = get_skill("2")
            if skill:
                return f"**{skill['title']}**\n\n{skill['content']}"
        if any(kw in text_lower for kw in ["safe", "scam", "fraud", "secure", "protect"]):
            skill = get_skill("4")
            if skill:
                return f"**{skill['title']}**\n\n{skill['content']}"
        if any(kw in text_lower for kw in ["government", "digilocker", "aadhaar", "document"]):
            skill = get_skill("3")
            if skill:
                return f"**{skill['title']}**\n\n{skill['content']}"
        if any(kw in text_lower for kw in ["basic", "smartphone", "internet", "start"]):
            skill = get_skill("1")
            if skill:
                return f"**{skill['title']}**\n\n{skill['content']}"
        return format_skills_for_chat()

    # chat (default)
    user_profile = dynamo.get_user_profile(user_id)
    return get_ai_response(
        message,
        language=language,
        session_id=session_id,
        user_id=user_id,
        chat_history=chat_history or [],
        user_profile=user_profile,
    )
