from pydantic import BaseModel, Field
from typing import Any
from enum import Enum


class UserBase(BaseModel):
    name: str = Field(None, title="Name", description="이름", example="홍길동")
    height: float = Field(
        None,
        title="Height",
        description="키(meter)",
        example=180.5,
        ge=0.0,
    )
    weight: float = Field(
        None,
        title="Weight",
        description="몸무게(kilogram)",
        example=80.5,
        ge=0.0,
    )
    age: int = Field(None, title="Age", description="나이", example=30, ge=0)
    gender: str = Field(None, title="Gender", description="성별", example="male")
    target_weight: float = Field(
        None,
        alias="targetWeight",
        title="Target Weight",
        description="목표 체중",
        example=65.0,
        ge=0.0,
    )


class UserCreate(UserBase):
    user_id: str | int = Field(..., title="User ID", description="유저 아이디")
    provider: str = Field(
        ..., title="Provider", description="소셜 로그인", examples="Naver"
    )
    access_token: str = Field(
        ..., title="Access Token", description="Social Access Token"
    )
    refresh_token: str = Field(
        ..., title="Refresh Token", description="Social Refresh Token"
    )


class UserRead(UserBase):
    pass


class UserUpdate(UserBase):
    access_token: str = Field(
        None, title="Access Token", description="Social Access Token"
    )
    refresh_token: str = Field(
        None, title="Refresh Token", description="Social Refresh Token"
    )
    jwt_refresh_token: str = Field(
        None, title="JWT Refresh Token", description="JWT Refresh Token"
    )


class UserResp(UserBase):
    pass


class UserUpdateReq(UserBase):
    pass


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
