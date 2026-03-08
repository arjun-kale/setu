"""
AI response: mock or call external AI service (LangGraph/RAG).
When AI_SERVICE_ENABLED=true and AI_SERVICE_URL set, calls AI service.
Otherwise uses mock. See docs/AI_INTEGRATION_CONTRACT.md.
"""

import json
import logging
import urllib.request
from decimal import Decimal
from typing import Any, Optional

from app.config import get_settings

logger = logging.getLogger("rural_ai_backend")

# Mock responses when AI service disabled or on error
_MOCK_RESPONSES = [
    "Thanks for your message. I'm the Rural AI Assistant. How can I help you todayΓÇöscheme search, eligibility check, or general questions?",
    "I'm here to help with government schemes and eligibility. You can ask things like 'What schemes are there for farmers?' or 'Am I eligible for PM-Kisan?'",
]


def _sanitize_for_json(obj: Any) -> Any:
    """Convert Decimal and other non-JSON types for serialization."""
    if obj is None:
        return None
    if isinstance(obj, Decimal):
        return int(obj) if obj == int(obj) else float(obj)
    if isinstance(obj, dict):
        return {k: _sanitize_for_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_sanitize_for_json(v) for v in obj]
    return obj


def _call_ai_service(
    message: str,
    language: str,
    session_id: str,
    user_id: str,
    chat_history: list[dict[str, Any]],
    user_profile: Optional[dict[str, Any]],
) -> Optional[str]:
    """Call AI service via HTTP. Returns response text or None on error."""
    settings = get_settings()
    url = (settings.ai_service_url or "").rstrip("/")
    if not url:
        return None
    timeout = settings.ai_service_timeout_sec
    endpoint = f"{url}/chat"

    # Build chat_history in contract format (role, content, created_at)
    history = []
    for item in chat_history or []:
        history.append({
            "role": item.get("role", "user"),
            "content": item.get("content", ""),
            "created_at": str(item.get("created_at", "")),
        })

    payload = {
        "message": message,
        "language": language,
        "session_id": session_id,
        "user_id": user_id,
        "chat_history": history,
        "user_profile": _sanitize_for_json(user_profile) if user_profile else None,
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            endpoint,
            data=data,
            method="POST",
            headers={"Content-Type": "application/json"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8")
            if resp.headers.get("Content-Type", "").startswith("application/json"):
                result = json.loads(body)
                return result.get("response") or str(result)
            return body.strip()
    except Exception as e:
        logger.warning("AI service call failed: %s", e)
        return None


def _mock_response(message: str) -> str:
    """Return mock response when AI disabled or on error."""
    msg = (message or "").strip()
    if not msg:
        return "Please send a message."
    idx = len(msg) % len(_MOCK_RESPONSES)
    return _MOCK_RESPONSES[idx]


def get_ai_response(
    message: str,
    language: str = "en",
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    chat_history: Optional[list[dict[str, Any]]] = None,
    user_profile: Optional[dict[str, Any]] = None,
) -> str:
    """
    AI response: calls external AI service when enabled, else mock.
    See docs/AI_INTEGRATION_CONTRACT.md for contract.
    """
    settings = get_settings()
    if settings.ai_service_enabled and settings.ai_service_url:
        response = _call_ai_service(
            message=message,
            language=language,
            session_id=session_id or "",
            user_id=user_id or "",
            chat_history=chat_history or [],
            user_profile=user_profile,
        )
        if response:
            return response
        # Fallback to mock on error
    return _mock_response(message)
