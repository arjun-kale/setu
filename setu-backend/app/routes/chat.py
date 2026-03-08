"""Chat API: POST /api/chat, GET /api/chat/history — session, store message, intent detection, response."""

from decimal import Decimal

from fastapi import APIRouter, Depends, Query

from app.config.database import get_db_session
from app.models.schemas import ChatHistoryResponse, ChatMessageOut, ChatRequest, ChatResponse
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service
from app.services.message_handler import process_message
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
    db: Session = Depends(get_db_session),
) -> ChatResponse:
    """
    Chat endpoint: user message → intent detection → scheme search / eligibility / AI → store → return.
    1. Check if user exists; create if not.
    2. Create session if needed.
    3. Store user message.
    4. Detect intent (scheme_search, eligibility_check, skill_learning, chat).
    5. Route to appropriate handler; get response.
    6. Store and return response.
    """
    user_id = body.user_id.strip()
    message = body.message.strip()
    language = body.language.strip() or "en"
    session_id = user_id

    if dynamo.get_user(user_id) is None:
        dynamo.create_user(user_id)

    dynamo.create_session(session_id, user_id=user_id)
    dynamo.save_message(session_id, "user", message)

    chat_history = dynamo.get_chat_history(session_id, limit=10)
    response = process_message(
        message,
        user_id=user_id,
        session_id=session_id,
        language=language,
        dynamo=dynamo,
        db=db,
        chat_history=chat_history,
    )

    dynamo.save_message(session_id, "assistant", response)
    return ChatResponse(response=response, session_id=session_id)


def _to_chat_message(item: dict) -> ChatMessageOut:
    """Convert DynamoDB item to ChatMessageOut (handles Decimal)."""
    created_at = item.get("created_at", "")
    if isinstance(created_at, Decimal):
        created_at = str(int(created_at))
    elif not isinstance(created_at, str):
        created_at = str(created_at)
    return ChatMessageOut(
        message_id=item.get("message_id", ""),
        role=item.get("role", "user"),
        content=item.get("content", ""),
        created_at=created_at,
    )


@router.get("/chat/history", response_model=ChatHistoryResponse)
def get_chat_history(
    session_id: str = Query(..., min_length=1, description="Session ID (e.g. user_id or whatsapp:+91...)"),
    limit: int = Query(default=50, ge=1, le=100, description="Max messages to return"),
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
) -> ChatHistoryResponse:
    """
    Get chat history for a session.
    Returns messages in chronological order (user and assistant).
    """
    items = dynamo.get_chat_history(session_id=session_id, limit=limit)
    messages = [_to_chat_message(item) for item in items]
    return ChatHistoryResponse(session_id=session_id, messages=messages)
