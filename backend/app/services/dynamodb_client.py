"""DynamoDB client for user sessions and chat history."""

import time
import uuid
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings

settings = get_settings()

_dynamo = boto3.resource(
    "dynamodb",
    region_name=settings.aws_region,
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
)


def get_sessions_table():
    """Return the sessions DynamoDB Table resource."""
    return _dynamo.Table(settings.dynamodb_table_sessions)


def get_chat_table():
    """Return the chat history DynamoDB Table resource."""
    return _dynamo.Table(settings.dynamodb_table_chat)


def create_tables_if_not_exist() -> tuple[bool, bool]:
    """
    Create sessions and chat_history tables if they do not exist.
    Returns (sessions_created, chat_created).
    """
    client = boto3.client(
        "dynamodb",
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )
    sessions_created = False
    chat_created = False

    try:
        client.describe_table(TableName=settings.dynamodb_table_sessions)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            client.create_table(
                TableName=settings.dynamodb_table_sessions,
                KeySchema=[{"AttributeName": "session_id", "KeyType": "HASH"}],
                AttributeDefinitions=[
                    {"AttributeName": "session_id", "AttributeType": "S"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            sessions_created = True
        else:
            raise

    try:
        client.describe_table(TableName=settings.dynamodb_table_chat)
    except ClientError as e:
        if e.response["Error"]["Code"] == "ResourceNotFoundException":
            client.create_table(
                TableName=settings.dynamodb_table_chat,
                KeySchema=[
                    {"AttributeName": "session_id", "KeyType": "HASH"},
                    {"AttributeName": "message_id", "KeyType": "RANGE"},
                ],
                AttributeDefinitions=[
                    {"AttributeName": "session_id", "AttributeType": "S"},
                    {"AttributeName": "message_id", "AttributeType": "S"},
                ],
                BillingMode="PAY_PER_REQUEST",
            )
            chat_created = True
        else:
            raise

    return sessions_created, chat_created


# --- Session helpers ---


def get_session(session_id: str) -> Optional[dict[str, Any]]:
    """Get a session by session_id. Returns None if not found."""
    table = get_sessions_table()
    try:
        r = table.get_item(Key={"session_id": session_id})
        return r.get("Item")
    except ClientError:
        return None


def put_session(
    session_id: str,
    *,
    user_id: Optional[str] = None,
    channel: Optional[str] = None,
    metadata: Optional[dict] = None,
) -> dict[str, Any]:
    """Create or update a session. Uses current timestamp for created_at/updated_at."""
    table = get_sessions_table()
    now = str(int(time.time()))
    existing = get_session(session_id)
    item = {
        "session_id": session_id,
        "created_at": existing.get("created_at", now) if existing else now,
        "updated_at": now,
    }
    if user_id is not None:
        item["user_id"] = user_id
    if channel is not None:
        item["channel"] = channel
    if metadata is not None:
        item["metadata"] = metadata
    table.put_item(Item=item)
    return item


# --- Chat history helpers ---


def add_chat_message(
    session_id: str,
    role: str,
    content: str,
    *,
    message_id: Optional[str] = None,
) -> dict[str, Any]:
    """Append a message to chat history. role: 'user' | 'assistant'. Returns the item."""
    table = get_chat_table()
    mid = message_id or str(uuid.uuid4())
    now = str(int(time.time()))
    item = {
        "session_id": session_id,
        "message_id": mid,
        "role": role,
        "content": content,
        "created_at": now,
    }
    table.put_item(Item=item)
    return item


def get_chat_history(
    session_id: str,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get recent messages for a session, ordered by message_id (chronological if UUID v7 or created_at)."""
    table = get_chat_table()
    r = table.query(
        KeyConditionExpression="session_id = :sid",
        ExpressionAttributeValues={":sid": session_id},
        Limit=limit,
        ScanIndexForward=True,
    )
    items = r.get("Items", [])
    # Sort by created_at if present for consistent order
    items.sort(key=lambda x: x.get("created_at", ""))
    return items
