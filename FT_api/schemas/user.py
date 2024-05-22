from pydantic import BaseModel, Field
from typing import Any, List, Dict, Optional
from datetime import date


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
    birthday: date = Field(
        None, title="Birthday", description="생년월일", example="1994-06-07"
    )
    gender: str = Field(None, title="Gender", description="성별", example="male")
    target_weight: float = Field(
        None,
        alias="targetWeight",
        title="Target Weight",
        description="목표 체중",
        example=65.0,
        ge=0.0,
    )
    blood_type: str = Field(
        None, alias="bloodType", title="Blood Type", description="혈액형", example="B"
    )


class UserCreate(UserBase):
    user_social_id: str | int = Field(
        ..., title="User Social ID", description="유저 아이디"
    )
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

class OptionRespSchema(BaseModel):
    id: int
    text: Optional[str]
    selected: Optional[bool]
    next_question_id: Optional[int]

class QuestionRespSchema(BaseModel):
    id: int
    text: Optional[str]
    page_number: Optional[int]
    options: List[OptionRespSchema]
    response: Optional[dict]  # {option_id, text_response, rating_response}

class SurveyRespSchema(BaseModel):
    id: int
    title: Optional[str]
    description: Optional[str]
    questions: List[QuestionRespSchema]

class UserRespSchema(BaseModel):
    user_id: int
    survey_id: int
    question_id: int
    option_id: int
    user_response: str
