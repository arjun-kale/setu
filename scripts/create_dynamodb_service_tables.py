"""Create DynamoDB tables for DynamoDBService: users, sessions, messages, user_profiles."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.services.dynamodb_service import DynamoDBService


def main() -> None:
    svc = DynamoDBService()
    result = svc.create_tables_if_not_exist()
    for name, created in result.items():
        print(f"{'Created' if created else 'Exists'}: {name}")
    print("DynamoDB service tables ready.")


if __name__ == "__main__":
    main()
