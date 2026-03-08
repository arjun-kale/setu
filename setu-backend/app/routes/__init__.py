"""API route modules."""

from fastapi import APIRouter

from app.routes import auth, chat, eligibility, health, schemes, skills, users, voice, webhooks

api_router = APIRouter()

# Health (no prefix)
api_router.include_router(health.router, tags=["health"])

# Webhooks: POST /webhooks/whatsapp (Twilio)
api_router.include_router(webhooks.router, tags=["webhooks"])

# Auth: POST /api/auth/register, POST /api/auth/login
api_router.include_router(auth.router, prefix="/api", tags=["auth"])

# Chat: POST /api/chat
api_router.include_router(chat.router, prefix="/api", tags=["chat"])

# User profile: PUT /api/users/{user_id}/profile
api_router.include_router(users.router, prefix="/api", tags=["users"])

# Voice: POST /api/voice
api_router.include_router(voice.router, prefix="/api", tags=["voice"])

# Scheme discovery: GET /api/schemes, GET /api/schemes/{id}
api_router.include_router(schemes.router, prefix="/api/schemes", tags=["schemes"])

# Eligibility: POST /api/check-eligibility
api_router.include_router(eligibility.router, prefix="/api/check-eligibility", tags=["eligibility"])

# Skills: GET /api/skills, GET /api/skills/{id}
api_router.include_router(skills.router, prefix="/api", tags=["skills"])
