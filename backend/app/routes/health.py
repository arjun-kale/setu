"""Health check endpoint for readiness and liveness."""

from datetime import datetime
from typing import Any

from fastapi import APIRouter
from sqlalchemy import text

from app import __version__
from app.config.database import get_db_session

router = APIRouter()


@router.get("/health", response_model=dict[str, Any])
def health() -> dict[str, Any]:
    """
    Health check endpoint.
    Use for load balancers, Kubernetes liveness/readiness, and monitoring.
    """
    return {
        "status": "healthy",
        "service": "rural-ai-assistant-backend",
        "version": __version__,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/health/db", response_model=dict[str, Any])
def health_db() -> dict[str, Any]:
    """Check PostgreSQL connectivity."""
    gen = get_db_session()
    db = next(gen)
    try:
        db.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception as e:
        db_status = f"error: {e!s}"
    finally:
        db.close()
    return {
        "status": "healthy" if db_status == "ok" else "degraded",
        "database": db_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


@router.get("/health/dynamo", response_model=dict[str, Any])
def health_dynamo() -> dict[str, Any]:
    """Check DynamoDB connectivity (sessions table exists and reachable)."""
    try:
        from app.services.dynamodb_client import get_sessions_table
        table = get_sessions_table()
        table.table_status
        dynamo_status = "ok"
    except Exception as e:
        dynamo_status = f"error: {e!s}"
    return {
        "status": "healthy" if dynamo_status == "ok" else "degraded",
        "dynamodb": dynamo_status,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }
