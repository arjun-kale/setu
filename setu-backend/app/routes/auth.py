"""Auth API: POST /api/auth/register, POST /api/auth/login."""

from fastapi import APIRouter, Depends, HTTPException

from app.models.schemas import LoginRequest, LoginResponse, RegisterRequest, RegisterResponse
from app.services.auth_service import create_access_token, hash_password, verify_password
from app.services.dynamodb_service import DynamoDBService, get_dynamodb_service

router = APIRouter()


def _normalize_email(email: str) -> str:
    return email.strip().lower()


@router.post("/auth/register", response_model=RegisterResponse)
def register(
    body: RegisterRequest,
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
):
    """Register a new user with email and password."""
    email = _normalize_email(body.email)
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    if len(body.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    user_id = email
    existing = dynamo.get_user(user_id)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    password_hash = hash_password(body.password)
    dynamo.create_user(
        user_id,
        email=email,
        name=body.name or "",
        password_hash=password_hash,
    )

    token = create_access_token(user_id=user_id, email=email)
    return RegisterResponse(
        user_id=user_id,
        email=email,
        token=token,
        message="Registration successful",
    )


@router.post("/auth/login", response_model=LoginResponse)
def login(
    body: LoginRequest,
    dynamo: DynamoDBService = Depends(get_dynamodb_service),
):
    """Login with email and password. Returns JWT token."""
    email = _normalize_email(body.email)
    if not email:
        raise HTTPException(status_code=400, detail="Email is required")

    user_id = email
    user = dynamo.get_user(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    password_hash = user.get("password_hash")
    if not password_hash:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not verify_password(body.password, password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    token = create_access_token(user_id=user_id, email=email)
    return LoginResponse(
        user_id=user_id,
        email=email,
        token=token,
        message="Login successful",
    )
