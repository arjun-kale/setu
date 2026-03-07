"""
Reusable DynamoDB service for FastAPI.
Tables: users, sessions, messages, user_profiles.
Region: ap-south-1 (configurable via DYNAMODB_REGION).
"""

import time
import uuid
from decimal import Decimal
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError

from app.config import get_settings


class DynamoDBService:
    """
    DynamoDB service for users, sessions, messages, and user_profiles.
    Use via dependency injection: DynamoDBService() or get_dynamodb_service().
    """

    def __init__(
        self,
        *,
        region: Optional[str] = None,
        table_users: Optional[str] = None,
        table_sessions: Optional[str] = None,
        table_messages: Optional[str] = None,
        table_user_profiles: Optional[str] = None,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
    ):
        settings = get_settings()
        self._region = region or settings.dynamodb_region
        self._table_users = table_users or settings.dynamodb_table_users
        self._table_sessions = table_sessions or "sessions"
        self._table_messages = table_messages or settings.dynamodb_table_messages
        self._table_user_profiles = (
            table_user_profiles or settings.dynamodb_table_user_profiles
        )
        self._access_key = aws_access_key_id or settings.aws_access_key_id
        self._secret_key = aws_secret_access_key or settings.aws_secret_access_key
        self._client = boto3.client(
            "dynamodb",
            region_name=self._region,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )
        self._resource = boto3.resource(
            "dynamodb",
            region_name=self._region,
            aws_access_key_id=self._access_key,
            aws_secret_access_key=self._secret_key,
        )

    def _users_table(self):
        return self._resource.Table(self._table_users)

    def _sessions_table(self):
        return self._resource.Table(self._table_sessions)

    def _messages_table(self):
        return self._resource.Table(self._table_messages)

    def _user_profiles_table(self):
        return self._resource.Table(self._table_user_profiles)

    def create_tables_if_not_exist(self) -> dict[str, bool]:
        """Create users, sessions, messages, user_profiles if they do not exist. Returns {table_name: created}."""
        result = {}

        for name, key_schema, attr_defs in [
            (
                self._table_users,
                [{"AttributeName": "user_id", "KeyType": "HASH"}],
                [{"AttributeName": "user_id", "AttributeType": "S"}],
            ),
            (
                self._table_sessions,
                [{"AttributeName": "session_id", "KeyType": "HASH"}],
                [{"AttributeName": "session_id", "AttributeType": "S"}],
            ),
            (
                self._table_messages,
                [
                    {"AttributeName": "session_id", "KeyType": "HASH"},
                    {"AttributeName": "message_id", "KeyType": "RANGE"},
                ],
                [
                    {"AttributeName": "session_id", "AttributeType": "S"},
                    {"AttributeName": "message_id", "AttributeType": "S"},
                ],
            ),
            (
                self._table_user_profiles,
                [{"AttributeName": "user_id", "KeyType": "HASH"}],
                [{"AttributeName": "user_id", "AttributeType": "S"}],
            ),
        ]:
            try:
                self._client.describe_table(TableName=name)
                result[name] = False
            except ClientError as e:
                if e.response["Error"]["Code"] == "ResourceNotFoundException":
                    self._client.create_table(
                        TableName=name,
                        KeySchema=key_schema,
                        AttributeDefinitions=attr_defs,
                        BillingMode="PAY_PER_REQUEST",
                    )
                    result[name] = True
                else:
                    raise

        return result

    # --- Users ---

    def create_user(
        self,
        user_id: str,
        *,
        email: Optional[str] = None,
        name: Optional[str] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Create a user. Returns the created item."""
        now = str(int(time.time()))
        item = {
            "user_id": user_id,
            "created_at": now,
            "updated_at": now,
        }
        if email is not None:
            item["email"] = email
        if name is not None:
            item["name"] = name
        item.update(extra)
        self._users_table().put_item(Item=item)
        return item

    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get a user by user_id. Returns None if not found."""
        try:
            r = self._users_table().get_item(Key={"user_id": user_id})
            return r.get("Item")
        except ClientError:
            return None

    # --- Sessions ---

    def create_session(
        self,
        session_id: str,
        *,
        user_id: Optional[str] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Create a session. Returns the created item."""
        now = str(int(time.time()))
        item = {
            "session_id": session_id,
            "created_at": now,
            "updated_at": now,
        }
        if user_id is not None:
            item["user_id"] = user_id
        item.update(extra)
        self._sessions_table().put_item(Item=item)
        return item

    # --- Messages (chat history) ---

    def save_message(
        self,
        session_id: str,
        role: str,
        content: str,
        *,
        message_id: Optional[str] = None,
        **extra: Any,
    ) -> dict[str, Any]:
        """Save a message (user or assistant). Returns the saved item."""
        mid = message_id or str(uuid.uuid4())
        now = str(int(time.time()))
        item = {
            "session_id": session_id,
            "message_id": mid,
            "role": role,
            "content": content,
            "created_at": now,
        }
        item.update(extra)
        self._messages_table().put_item(Item=item)
        return item

    def get_chat_history(
        self,
        session_id: str,
        limit: int = 50,
    ) -> list[dict[str, Any]]:
        """Get messages for a session, ordered by created_at."""
        r = self._messages_table().query(
            KeyConditionExpression="session_id = :sid",
            ExpressionAttributeValues={":sid": session_id},
            Limit=limit,
            ScanIndexForward=True,
        )
        items = r.get("Items", [])
        items.sort(key=lambda x: x.get("created_at", ""))
        return items

    # --- User profiles ---

    def get_user_profile(self, user_id: str) -> Optional[dict[str, Any]]:
        """Get user profile (age, income, state, occupation, etc.). Returns None if not found."""
        try:
            r = self._user_profiles_table().get_item(Key={"user_id": user_id})
            return r.get("Item")
        except ClientError:
            return None

    def update_user_profile(self, user_id: str, **profile_data: Any) -> dict[str, Any]:
        """Create or update user profile. Merges with existing. Pass age, income, state, occupation, etc."""
        now = str(int(time.time()))
        table = self._user_profiles_table()
        # DynamoDB requires Decimal for numbers, not float
        safe_data = {}
        for k, v in profile_data.items():
            if isinstance(v, float):
                safe_data[k] = Decimal(str(v))
            else:
                safe_data[k] = v
        try:
            r = table.get_item(Key={"user_id": user_id})
            existing = r.get("Item") or {}
        except ClientError:
            existing = {}
        existing.update(safe_data)
        existing["user_id"] = user_id
        existing["updated_at"] = now
        if "created_at" not in existing:
            existing["created_at"] = now
        table.put_item(Item=existing)
        return existing


def get_dynamodb_service() -> DynamoDBService:
    """FastAPI dependency: return a DynamoDBService instance."""
    return DynamoDBService()
