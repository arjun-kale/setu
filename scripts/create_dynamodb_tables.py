"""Create DynamoDB tables for sessions and chat history if they do not exist."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.dynamodb_client import create_tables_if_not_exist


def main() -> None:
    sessions_created, chat_created = create_tables_if_not_exist()
    if sessions_created:
        print("Created table: rural_ai_sessions (or DYNAMODB_TABLE_SESSIONS)")
    else:
        print("Sessions table already exists.")
    if chat_created:
        print("Created table: rural_ai_chat_history (or DYNAMODB_TABLE_CHAT)")
    else:
        print("Chat table already exists.")
    print("DynamoDB setup done.")


if __name__ == "__main__":
    main()
