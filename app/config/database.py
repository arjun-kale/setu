"""PostgreSQL session and engine (SQLAlchemy)."""

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

settings = get_settings()
DATABASE_URL = settings.postgres_url

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db_session():
    """Sync session dependency for FastAPI."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
