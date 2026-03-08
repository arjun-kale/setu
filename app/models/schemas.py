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


class ChatMessageOut(BaseModel):
    """Single message in chat history."""

    message_id: str = Field(..., description="Message ID")
    role: str = Field(..., description="user or assistant")
    content: str = Field(..., description="Message content")
    created_at: str = Field(..., description="Timestamp")


class ChatHistoryResponse(BaseModel):
    """GET /api/chat/history response."""

    session_id: str = Field(..., description="Session ID")
    messages: list[ChatMessageOut] = Field(default_factory=list, description="Chat messages in chronological order")


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


# --- Eligibility check ---


class CheckEligibilityRequest(BaseModel):
    """POST /api/check-eligibility body."""

    age: int | None = Field(None, ge=0, le=120, description="User age")
    income: float | None = Field(None, ge=0, description="Annual income")
    state: str | None = Field(None, description="State (e.g. MH, KA)")
    occupation: str | None = Field(None, description="Occupation (e.g. farmer, student)")


class CheckEligibilityResponse(BaseModel):
    """POST /api/check-eligibility response."""

    schemes: list[SchemeOut] = Field(default_factory=list, description="Matching schemes")


# --- Auth ---


class RegisterRequest(BaseModel):
    """POST /api/auth/register body."""

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=6)
    name: str | None = Field(None)


class RegisterResponse(BaseModel):
    user_id: str
    email: str
    token: str
    message: str


class LoginRequest(BaseModel):
    """POST /api/auth/login body."""

    email: str = Field(..., min_length=1)
    password: str = Field(..., min_length=1)


class LoginResponse(BaseModel):
    user_id: str
    email: str
    token: str
    message: str


# --- User profile ---


class UpdateProfileRequest(BaseModel):
    """PUT /api/users/{user_id}/profile body."""

    age: int | None = Field(None, ge=0, le=120)
    income: float | None = Field(None, ge=0)
    state: str | None = None
    occupation: str | None = None
