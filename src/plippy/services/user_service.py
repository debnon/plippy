from sqlalchemy.orm import Session

from plippy.models import User
from plippy.repositories.user_repository import UserRepository
from plippy.schemas.user import CreateUserRequest


class UserService:
    def __init__(self, session: Session) -> None:
        self._repo = UserRepository(session)

    def create_user(self, payload: CreateUserRequest) -> User:
        return self._repo.create_user(name=payload.name, funds=payload.funds)

    def list_users(self) -> list[User]:
        return self._repo.list_users()
