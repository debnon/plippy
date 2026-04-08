from decimal import Decimal

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from db import Base
from models import User


def test_user_model_can_roundtrip_in_sqlite() -> None:
    engine = create_engine("sqlite+pysqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        session.add(User(name="ben", funds=Decimal("50.25")))
        session.commit()

        saved = session.execute(select(User).where(User.name == "ben")).scalar_one()
        assert saved.funds == Decimal("50.25")