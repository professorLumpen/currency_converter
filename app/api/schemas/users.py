from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    username: str = Field(max_length=30, min_length=5)
    password: str = Field(min_length=10)


class UserCreate(UserBase):
    pass


class UserFromDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    register_date: datetime


class UserLogin(UserBase):
    pass


class Token(BaseModel):
    token: str
    type: str = "bearer"
