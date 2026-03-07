"""Chat API: POST /api/chat — session, store message, intent detection, response, store and return."""

from fastapi import APIRouter, Depends

from app.config.database import get_db_session
from app.models.schemas import ChatRequest, ChatResponse
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
