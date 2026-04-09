from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from plippy.models import User


class UserRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_user(self, name: str, funds: Decimal) -> User:
        user = User(name=name, funds=funds)
        self._session.add(user)
        self._session.commit()
        self._session.refresh(user)
        return user

    def list_users(self) -> list[User]:
        stmt = select(User).order_by(User.id)
        return self._session.scalars(stmt).all()
