"""PostgreSQL models for government schemes and eligibility rules."""

from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Scheme(Base):
    """Government scheme — metadata and display info."""

    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    slug = Column(String(255), unique=True, nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(128), nullable=True, index=True)  # e.g. farmer, education, health
    state = Column(String(64), nullable=True, index=True)  # null = national
    source_url = Column(String(512), nullable=True)
    is_active = Column(Integer, default=1)  # 1=active, 0=inactive
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    eligibility_rules = relationship("EligibilityRule", back_populates="scheme", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Scheme(id={self.id}, name={self.name!r})>"


class EligibilityRule(Base):
    """Eligibility rules for a scheme (age, income, state, occupation)."""

    __tablename__ = "eligibility_rules"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(Integer, ForeignKey("schemes.id", ondelete="CASCADE"), nullable=False, index=True)
    min_age = Column(Integer, nullable=True)
    max_age = Column(Integer, nullable=True)
    min_income = Column(Float, nullable=True)
    max_income = Column(Float, nullable=True)
    states = Column(JSON, nullable=True)  # list of state codes, e.g. ["MH", "KA"]; null = all
    occupations = Column(JSON, nullable=True)  # list of occupation keywords; null = any
    extra_criteria = Column(JSON, nullable=True)  # flexible key-value for other rules
    created_at = Column(DateTime, default=datetime.utcnow)

    scheme = relationship("Scheme", back_populates="eligibility_rules")

    def __repr__(self) -> str:
        return f"<EligibilityRule(id={self.id}, scheme_id={self.scheme_id})>"
