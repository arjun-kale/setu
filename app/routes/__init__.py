"""API route modules."""

from fastapi import APIRouter

from app.routes import chat, eligibility, health, schemes, voice

api_router = APIRouter()

# Health (no prefix)
api_router.include_router(health.router, tags=["health"])

# Chat: POST /api/chat
api_router.include_router(chat.router, prefix="/api", tags=["chat"])

# Voice: POST /api/voice
api_router.include_router(voice.router, prefix="/api", tags=["voice"])

# Scheme discovery: GET /api/schemes, GET /api/schemes/{id}
api_router.include_router(schemes.router, prefix="/api/schemes", tags=["schemes"])

# Eligibility: POST /api/check-eligibility
api_router.include_router(eligibility.router, prefix="/api/check-eligibility", tags=["eligibility"])
