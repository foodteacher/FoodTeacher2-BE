from pydantic import BaseModel
from typing import Optional, Any

class UserBase(BaseModel):
    id: int | None = None

class UserCreate(UserBase):
    user_id: str| int
    provider: str
    access_token: str
    refresh_token: str

class UserUpdate(UserBase):
    name: str | None = None
    height: float | None = None
    weight: float | None = None
    age: int | None = None
    gender: str | None = None
    target_weight: float | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    jwt_refresh_token: str | None = None

class UserInput(BaseModel):
    query: str

class UserInDBBase(BaseModel):
    name: str| None = None
    height: float | None = None
    weight: float | None = None
    age: int | None = None
    gender: str | None = None
    target_weight: float | None = None

    class Config:
        from_attributes = True


class UserRead(UserInDBBase):
    pass

class UserInfo(BaseModel):
    name: str | None = None
    gender: str | None = None
    age: int | None = None
    height: float | None = None
    weight: float | None = None
    target_weight: float | None = None
    breakfast: dict[str, Any] | None = None
    lunch: dict[str, Any] | None = None
    dinner: dict[str, Any] | None = None
    advice: str | None = None
    recommended_exercise: str | None = None
    excess_calories: float | None = None
