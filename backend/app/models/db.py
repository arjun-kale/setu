"""SQLAlchemy models for PostgreSQL (government schemes, eligibility rules)."""

from app.config.database import Base
from app.models.scheme import EligibilityRule, Scheme

__all__ = ["Base", "EligibilityRule", "Scheme"]
