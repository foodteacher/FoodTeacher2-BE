from pydantic import BaseModel, Field
from typing import Optional
from datetime import date


class UserBase(BaseModel):
    name: Optional[str] = Field(
        None, title="Name", description="이름", example="홍길동"
    )
    height: Optional[float] = Field(
        None,
        title="Height",
        description="키(meter)",
        example=180.5,
        ge=0.0,
    )
    weight: Optional[float] = Field(
        None,
        title="Weight",
        description="몸무게(kilogram)",
        example=80.5,
        ge=0.0,
    )
    birthday: Optional[date] = Field(
        None, title="Birthday", description="생년월일", example="1994-06-07"
    )
    gender: Optional[str] = Field(
        None, title="Gender", description="성별", example="male"
    )
    target_weight: Optional[float] = Field(
        None,
        serialization_alias="targetWeight",
        title="Target Weight",
        description="목표 체중",
        example=65.0,
        ge=0.0,
    )
    blood_type: Optional[str] = Field(
        None,
        serialization_alias="bloodType",
        title="Blood Type",
        description="혈액형",
        example="B",
    )


class UserCreate(UserBase):
    user_social_id: str | int = Field(
        ..., title="User Social ID", description="유저 아이디"
    )
    provider: str = Field(
        ..., title="Provider", description="소셜 로그인", examples="Naver"
    )
    social_access_token: str = Field(
        ..., title="Social Access Token", description="Social Access Token"
    )
    social_refresh_token: str = Field(
        ..., title="Social Refresh Token", description="Social Refresh Token"
    )


class UserRead(UserBase):
    pass


class UserUpdate(UserBase):
    social_access_token: str = Field(
        None, title="Social Access Token", description="Social Access Token"
    )
    social_refresh_token: str = Field(
        None, title="SocialRefresh Token", description="Social Refresh Token"
    )


class UserResp(UserBase):
    pass


class UserUpdateReq(UserBase):
    pass
