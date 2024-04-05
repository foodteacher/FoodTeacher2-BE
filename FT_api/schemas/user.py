from pydantic import BaseModel
from typing import Optional, Any, Union

class UserBase(BaseModel):
    id: Optional[int] = None

class UserCreate(UserBase):
    user_id: Union[str, int]
    provider: str
    access_token: str
    refresh_token: str
    jwt_refresh_token: str

class UserUpdate(UserBase):
    name: str = None
    height: float = None
    weight: float = None
    age: int = None
    gender: str = None
    target_weight: float = None
    access_token: str = None
    refresh_token: str = None
    jwt_refresh_token: str = None

class UserInput(BaseModel):
    query: str

class UserInDBBase(BaseModel):
    name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    target_weight: Optional[float] = None

    class Config:
        from_attributes = True


class UserRead(UserInDBBase):
    pass

class UserInfo(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    age: Optional[int] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    target_weight: Optional[float] = None
    breakfast: Optional[dict[str, Any]] = None
    lunch: Optional[dict[str, Any]] = None
    dinner: Optional[dict[str, Any]] = None
    advice: Optional[str] = None
    recommended_exercise: Optional[str] = None
    excess_calories: Optional[float] = None
