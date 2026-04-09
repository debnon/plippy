from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    funds: Decimal = Decimal("0.00")


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    funds: Decimal
