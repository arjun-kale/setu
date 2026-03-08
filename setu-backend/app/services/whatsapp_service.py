"""Twilio WhatsApp API: send message via REST."""

import logging
from typing import Optional

from app.config import get_settings

logger = logging.getLogger("rural_ai_backend")


def send_whatsapp_message(to: str, body: str) -> bool:
    """
    Send a WhatsApp message via Twilio.
    to: e.g. whatsapp:+919923410767
    body: message text
    Returns True if sent, False on error.
    """
    try:
        from twilio.rest import Client
    except ImportError:
        return False

    settings = get_settings()
    if not settings.twilio_account_sid or not settings.twilio_auth_token:
        return False

    client = Client(
        settings.twilio_account_sid,
        settings.twilio_auth_token,
    )
    from_num = settings.twilio_whatsapp_number or "whatsapp:+14155238886"

    try:
        client.messages.create(
            body=body,
            from_=from_num,
            to=to,
        )
        logger.info("WhatsApp message sent to %s", to)
        return True
    except Exception as e:
        logger.exception("Twilio send failed: %s", e)
        return False
