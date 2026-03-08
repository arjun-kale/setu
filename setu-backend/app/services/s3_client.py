"""S3 client for audio file storage. Upload voice input/output for audit and replay."""

import time
from typing import Optional

import boto3

from app.config import get_settings


def _get_client():
    settings = get_settings()
    return boto3.client(
        "s3",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


def upload_audio(
    data: bytes,
    *,
    user_id: str,
    session_id: str,
    suffix: str,
    content_type: str = "application/octet-stream",
) -> Optional[str]:
    """
    Upload audio to S3. Returns the S3 key (path) or None if upload fails.
    Key format: voice/{user_id}/{session_id}/{timestamp}_{suffix}
    """
    try:
        settings = get_settings()
        client = _get_client()
        ts = int(time.time() * 1000)
        key = f"voice/{user_id}/{session_id}/{ts}_{suffix}"
        client.put_object(
            Bucket=settings.s3_bucket_name,
            Key=key,
            Body=data,
            ContentType=content_type,
        )
        return key
    except Exception:
        return None


def get_presigned_url(key: str, expires_in: int = 3600) -> Optional[str]:
    """Generate a presigned URL to download the audio. Expires in 1 hour by default."""
    try:
        settings = get_settings()
        client = _get_client()
        url = client.generate_presigned_url(
            "get_object",
            Params={"Bucket": settings.s3_bucket_name, "Key": key},
            ExpiresIn=expires_in,
        )
        return url
    except Exception:
        return None
