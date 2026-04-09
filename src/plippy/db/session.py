import os
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/plippy"

database_url = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
