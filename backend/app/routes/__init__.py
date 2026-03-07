"""API route modules."""

from fastapi import APIRouter

from app.routes import health

api_router = APIRouter()

# Health (no prefix, often at /health)
api_router.include_router(health.router, tags=["health"])

# Future route modules (uncomment and add prefix when implemented):
# from app.routes import chat, voice, schemes, eligibility, whatsapp
# api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
# api_router.include_router(voice.router, prefix="/voice", tags=["voice"])
# api_router.include_router(schemes.router, prefix="/schemes", tags=["schemes"])
# api_router.include_router(eligibility.router, prefix="/eligibility", tags=["eligibility"])
# api_router.include_router(whatsapp.router, prefix="/webhooks/whatsapp", tags=["whatsapp"])
