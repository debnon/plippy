import os
from decimal import Decimal

import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from plippy.db import Base
from plippy.models import User


@pytest.mark.integration
def test_user_model_can_roundtrip_in_postgres() -> None:
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        pytest.skip("DATABASE_URL is not set")

    engine = create_engine(database_url)
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(name="integration-test-user", funds=Decimal("10.00"))
        session.add(user)
        session.commit()

        found = session.execute(select(User).where(User.id == user.id)).scalar_one()
        assert found.funds == Decimal("10.00")

        session.delete(found)
        session.commit()