from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from plippy.api.deps import get_db_session
from plippy.schemas.user import CreateUserRequest, UserResponse
from plippy.services.user_service import UserService


router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserResponse)
def create_user(
    payload: CreateUserRequest,
    session: Session = Depends(get_db_session),
) -> UserResponse:
    service = UserService(session)
    user = service.create_user(payload)
    return UserResponse.model_validate(user)


@router.get("", response_model=list[UserResponse])
def list_users(session: Session = Depends(get_db_session)) -> list[UserResponse]:
    service = UserService(session)
    users = service.list_users()
    return [UserResponse.model_validate(user) for user in users]
