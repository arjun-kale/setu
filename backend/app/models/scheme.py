"""PostgreSQL models for government schemes, eligibility, and documents."""

from sqlalchemy import Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.config.database import Base


class Scheme(Base):
    """Government scheme — id, name, description, benefits."""

    __tablename__ = "schemes"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    benefits = Column(Text, nullable=True)

    eligibility = relationship(
        "SchemeEligibility",
        back_populates="scheme",
        cascade="all, delete-orphan",
    )
    documents = relationship(
        "SchemeDocument",
        back_populates="scheme",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Scheme(id={self.id}, name={self.name!r})>"


class SchemeEligibility(Base):
    """Eligibility criteria for a scheme."""

    __tablename__ = "scheme_eligibility"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(
        Integer,
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    age_limit = Column(String(128), nullable=True)
    income_limit = Column(String(128), nullable=True)
    state = Column(String(128), nullable=True, index=True)
    occupation = Column(String(255), nullable=True, index=True)

    scheme = relationship("Scheme", back_populates="eligibility")

    def __repr__(self) -> str:
        return f"<SchemeEligibility(id={self.id}, scheme_id={self.scheme_id})>"


class SchemeDocument(Base):
    """Documents linked to a scheme."""

    __tablename__ = "scheme_documents"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    scheme_id = Column(
        Integer,
        ForeignKey("schemes.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    document_name = Column(String(255), nullable=False)
    document_url = Column(String(512), nullable=True)

    scheme = relationship("Scheme", back_populates="documents")

    def __repr__(self) -> str:
        return f"<SchemeDocument(id={self.id}, scheme_id={self.scheme_id})>"
