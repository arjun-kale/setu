"""DynamoDB client for user sessions and chat history."""

# import boto3
# from app.config import get_settings
#
# settings = get_settings()
# _dynamo = boto3.resource("dynamodb", region_name=settings.aws_region)
#
# def get_sessions_table():
#     return _dynamo.Table(settings.dynamodb_table_sessions)
#
# def get_chat_table():
#     return _dynamo.Table(settings.dynamodb_table_chat)
