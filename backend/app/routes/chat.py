"""Chat API: POST /api/chat — session, store message, AI response, store and return."""

from fastapi import APIRouter, Depends

from app.models.schemas import ChatRequest, ChatResponse
from app.services.ai_agent import get_ai_response
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service

router = APIRouter()


@router.post("/chat", response_model=ChatResponse)
def chat(
    body: ChatRequest,
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
) -> ChatResponse:
    """
    Chat endpoint: user message → session + store → AI response → store → return.
    1. Check if user exists in DynamoDB; create user if not.
    2. Create session if needed (one session per user: session_id = user_id).
    3. Store user message in messages table.
    4. Call AI service for response.
    5. Store AI response in DynamoDB.
    6. Return response.
    """
    user_id = body.user_id.strip()
    message = body.message.strip()
    language = body.language.strip() or "en"
    session_id = user_id  # one active session per user

    # 1. Check if user exists; create if not
    if dynamo.get_user(user_id) is None:
        dynamo.create_user(user_id)

    # 2. Create session if needed (idempotent put)
    dynamo.create_session(session_id, user_id=user_id)

    # 3. Store user message in messages table
    dynamo.save_message(session_id, "user", message)

    # 4. Call AI service for response
    chat_history = dynamo.get_chat_history(session_id, limit=10)
    ai_response = get_ai_response(
        message,
        language=language,
        session_id=session_id,
        user_id=user_id,
        chat_history=chat_history,
    )

    # 5. Store AI response in DynamoDB
    dynamo.save_message(session_id, "assistant", ai_response)

    # 6. Return response
    return ChatResponse(response=ai_response, session_id=session_id)
