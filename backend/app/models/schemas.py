"""Pydantic request/response schemas (placeholder for chat, voice, schemes, etc.)."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = "healthy"
    service: str = "rural-ai-assistant-backend"
    version: str
    timestamp: str


class ChatRequest(BaseModel):
    """POST /api/chat body."""

    user_id: str = Field(..., min_length=1, description="User identifier")
    message: str = Field(..., min_length=1, description="User message")
    language: str = Field(default="en", description="Language code (e.g. en, hi)")


class ChatResponse(BaseModel):
    """POST /api/chat response."""

    response: str = Field(..., description="AI assistant response")
    session_id: str = Field(..., description="Session id used for this conversation")


# --- Scheme discovery ---


class EligibilityRuleOut(BaseModel):
    """Eligibility rule in scheme response."""

    age_limit: str | None = None
    income_limit: str | None = None
    state: str | None = None
    occupation: str | None = None


class SchemeOut(BaseModel):
    """Scheme in list and detail responses."""

    id: int
    name: str
    description: str | None = None
    benefits: str | None = None
    eligibility_rules: list[EligibilityRuleOut] = Field(default_factory=list)


class SchemeListResponse(BaseModel):
    """GET /api/schemes response."""

    schemes: list[SchemeOut]
