import os

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


DEFAULT_DATABASE_URL = "postgresql+psycopg://postgres:postgres@localhost:5432/plippy"


class Base(DeclarativeBase):
    pass


database_url = os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL)
engine = create_engine(database_url, echo=False)
SessionLocal = sessionmaker(bind=engine)


def init_db() -> None:
    import models

    _ = models.User

    Base.metadata.create_all(engine)