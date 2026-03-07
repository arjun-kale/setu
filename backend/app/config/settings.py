"""Application settings loaded from environment variables via python-dotenv."""

from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings

# Load .env from backend root (parent of app/) so variables are available to Settings
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

    # Google Speech-to-Text (optional until you add key)
    google_stt_api_key: Optional[str] = Field(default=None, alias="GOOGLE_STT_API_KEY")

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "extra": "ignore",
    }


@lru_cache
def get_settings() -> Settings:
    """Cached settings instance (loaded from env via python-dotenv)."""
    return Settings()
