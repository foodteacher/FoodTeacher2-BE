from pydantic import BaseModel
from typing import Optional, Any

class UserBase(BaseModel):
    id: Optional[int] = None

class UserCreate(UserBase):
    kakao_id: int
    kakao_access_token: str
    kakao_refresh_token: str
    jwt_refresh_token: str

class UserUpdate(UserBase):
    name: str = None
    height: float = None
    weight: float = None
    age: int = None
    gender: str = None
    target_weight: float = None
    kakao_access_token: str = None
    kakao_refresh_token: str = None
    jwt_refresh_token: str = None

class UserInput(BaseModel):
    query: str

class UserInDBBase(UserBase):
    kakao_id: Optional[int] = None
    name: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    age: Optional[int] = None
    gender: Optional[str] = None
    target_weight: Optional[float] = None
    kakao_access_token: Optional[str] = None
    kakao_refresh_token: Optional[str] = None
    jwt_refresh_token: Optional[str] = None

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