"""
Mock AI response for chat API.
Later: replace with teammate's AI agent API (LangGraph + Pinecone RAG).
"""

from typing import Any, Optional

# Mock responses by intent/keyword for a more realistic demo (optional).
_MOCK_RESPONSES = [
    "Thanks for your message. I'm the Rural AI Assistant. How can I help you today—scheme search, eligibility check, or general questions?",
    "I'm here to help with government schemes and eligibility. You can ask things like 'What schemes are there for farmers?' or 'Am I eligible for PM-Kisan?'",
]


def get_ai_response(
    message: str,
    language: str = "en",
    *,
    session_id: Optional[str] = None,
    user_id: Optional[str] = None,
    chat_history: Optional[list[dict[str, Any]]] = None,
) -> str:
    """
    Mock AI response. Replace with real AI agent API when integrated.
    """
    _ = session_id, user_id, chat_history
    msg = (message or "").strip()
    if not msg:
        return "Please send a message."
    # Simple deterministic mock: use message length to pick a response for variety
    idx = len(msg) % len(_MOCK_RESPONSES)
    return _MOCK_RESPONSES[idx]
