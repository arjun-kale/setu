"""Application settings loaded from environment variables via python-dotenv."""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

# Load .env from project root (parent of app/) so variables are available to Settings
_env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(dotenv_path=_env_path)


class Settings(BaseSettings):
    """Central configuration for rural-ai-assistant-backend."""

    app_name: str = Field(default="rural-ai-assistant-backend", alias="APP_NAME")

    # AWS
    aws_access_key_id: str = Field(..., alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(..., alias="AWS_REGION")

    # PostgreSQL (single URL)
    postgres_url: str = Field(..., alias="POSTGRES_URL")

    # S3
    s3_bucket_name: str = Field(..., alias="S3_BUCKET_NAME")

    # DynamoDB (legacy: sessions & chat history)
    dynamodb_table_sessions: str = Field(
        default="rural_ai_sessions", alias="DYNAMODB_TABLE_SESSIONS"
    )
    dynamodb_table_chat: str = Field(
        default="rural_ai_chat_history", alias="DYNAMODB_TABLE_CHAT"
    )
    # DynamoDB service (users, sessions, messages, user_profiles) — region ap-south-1
    dynamodb_region: str = Field(default="ap-south-1", alias="DYNAMODB_REGION")
    dynamodb_table_users: str = Field(default="users", alias="DYNAMODB_TABLE_USERS")
    dynamodb_table_messages: str = Field(
        default="messages", alias="DYNAMODB_TABLE_MESSAGES"
    )
    dynamodb_table_user_profiles: str = Field(
        default="user_profiles", alias="DYNAMODB_TABLE_USER_PROFILES"
    )

    # Twilio WhatsApp (optional until you add keys)
    twilio_account_sid: Optional[str] = Field(default=None, alias="TWILIO_ACCOUNT_SID")
    twilio_auth_token: Optional[str] = Field(default=None, alias="TWILIO_AUTH_TOKEN")
    twilio_whatsapp_number: Optional[str] = Field(default=None, alias="TWILIO_WHATSAPP_NUMBER")

    # Speech-to-Text: whisper (free, local) or google (requires billing)
    stt_provider: str = Field(default="whisper", alias="STT_PROVIDER")
    whisper_model_size: str = Field(default="base", alias="WHISPER_MODEL_SIZE")

    # Google Speech-to-Text (only when STT_PROVIDER=google)
    google_application_credentials: Optional[str] = Field(
        default=None, alias="GOOGLE_APPLICATION_CREDENTIALS"
    )

    # Amazon Polly voice (optional)
    polly_voice_id: str = Field(default="Joanna", alias="POLLY_VOICE_ID")

    # Auth (JWT)
    jwt_secret: str = Field(default="change-me-in-production", alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", alias="JWT_ALGORITHM")
    jwt_expire_hours: int = Field(default=24, alias="JWT_EXPIRE_HOURS")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (loaded from env via python-dotenv)."""
    return Settings()
