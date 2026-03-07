"""Pydantic request/response schemas (placeholder for chat, voice, schemes, etc.)."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str = "rural-ai-assistant-backend"
    version: str
    timestamp: str
