from pydantic import BaseModel, Field
from typing import Any
from enum import Enum


class UserBase(BaseModel):
    id: int | None = None


class UserCreate(UserBase):
    user_id: str | int
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
    name: str | None = None
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


# class HealthGoalOption(Enum):
#     근력강화 = "근력강화"
#     건강유지 = "건강유지"
#     체중감량 = "체중감량"
#     아직_목표가_없어요 = "아직 목표가 없어요"
#     직접_입력할래요 = "직접 입력할래요"


# class HealthGoal(BaseModel):
#     goal: HealthGoalOption = Field(
#         ..., example="근력강화", description="사용자의 건강 목표"
#     )


# # 예시: Pydantic 모델을 확장하여 사용자 입력을 받는 경우
# class CustomHealthGoal(BaseModel):
#     custom_goal: str = Field(
#         ..., example="마라톤 완주", description="사용자가 직접 입력한 건강 목표"
#     )
