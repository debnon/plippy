from decimal import Decimal
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import select

from db import SessionLocal, init_db
from models import User


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(title="plippy API", lifespan=lifespan)


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    funds: Decimal = Decimal("0.00")


class UserResponse(BaseModel):
    id: int
    name: str
    funds: Decimal


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/users", response_model=UserResponse)
def create_user(payload: CreateUserRequest) -> UserResponse:
    with SessionLocal() as session:
        user = User(name=payload.name, funds=payload.funds)
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserResponse(id=user.id, name=user.name, funds=user.funds)


@app.get("/users", response_model=list[UserResponse])
def list_users() -> list[UserResponse]:
    with SessionLocal() as session:
        users = session.scalars(select(User).order_by(User.id)).all()
        return [UserResponse(id=u.id, name=u.name, funds=u.funds) for u in users]