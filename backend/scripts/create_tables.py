"""Create PostgreSQL tables for schemes and eligibility_rules. Run once after DB is ready."""

import sys
from pathlib import Path

# Add backend root so app is importable
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config.database import Base, engine
from app.models.db import EligibilityRule, Scheme  # noqa: F401 — register models


def main() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables created: schemes, eligibility_rules")


if __name__ == "__main__":
    main()
