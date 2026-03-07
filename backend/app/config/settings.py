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

    # AWS
    aws_access_key_id: str = Field(..., alias="AWS_ACCESS_KEY_ID")
    aws_secret_access_key: str = Field(..., alias="AWS_SECRET_ACCESS_KEY")
    aws_region: str = Field(..., alias="AWS_REGION")

    # PostgreSQL (single URL)
    postgres_url: str = Field(..., alias="POSTGRES_URL")

    # S3
    s3_bucket_name: str = Field(..., alias="S3_BUCKET_NAME")

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
