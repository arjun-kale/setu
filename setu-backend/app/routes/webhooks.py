"""Webhooks: POST /webhooks/whatsapp — Twilio WhatsApp incoming messages."""

import logging

from fastapi import APIRouter, Depends, Form, Request

from app.config.database import get_db_session

logger = logging.getLogger("rural_ai_backend")
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service
from app.services.message_handler import process_message
from app.services.whatsapp_service import send_whatsapp_message
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/webhooks/whatsapp")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(..., alias="From"),
    Body: str = Form(default="", alias="Body"),
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
    db: Session = Depends(get_db_session),
):
    """
    Twilio WhatsApp webhook. Receives incoming messages, runs chat flow, sends reply.
    Map From (whatsapp:+91...) to user_id for session.
    """
    message = (Body or "").strip()
    if not message:
        return {"status": "ok"}

    # user_id = WhatsApp number (e.g. whatsapp:+919923410767)
    user_id = From.strip()
    session_id = user_id

    # Ensure user exists
    if dynamo.get_user(user_id) is None:
        dynamo.create_user(user_id)
    dynamo.create_session(session_id, user_id=user_id)
    dynamo.save_message(session_id, "user", message)

    # Process message (intent detection → scheme/eligibility/skill/chat)
    chat_history = dynamo.get_chat_history(session_id, limit=10)
    response = process_message(
        message,
        user_id=user_id,
        session_id=session_id,
        language="en-IN",
        dynamo=dynamo,
        db=db,
        chat_history=chat_history,
    )

    dynamo.save_message(session_id, "assistant", response)

    # Send reply via Twilio (strip markdown for WhatsApp)
    reply = response.replace("**", "").strip()
    sent = send_whatsapp_message(to=user_id, body=reply)
    if not sent:
        logger.warning("Failed to send WhatsApp reply to %s", user_id)

    return {"status": "ok"}
