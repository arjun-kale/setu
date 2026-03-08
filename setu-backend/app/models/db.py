"""SQLAlchemy models for PostgreSQL (schemes, eligibility, documents)."""

from app.config.database import Base
from app.models.scheme import Scheme, SchemeDocument, SchemeEligibility

__all__ = ["Base", "Scheme", "SchemeEligibility", "SchemeDocument"]
