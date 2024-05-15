from typing import Optional
from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from pydantic import validator

# from FT_api.schemas.user import HealthGoal, CustomHealthGoal


from FT_api.db.session import Base


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    user_id: Mapped[str] = mapped_column(String(255))
    provider: Mapped[str] = mapped_column(String(255))
    access_token: Mapped[str] = mapped_column(String(255))
    refresh_token: Mapped[str] = mapped_column(String(255))
    jwt_refresh_token: Mapped[str] = mapped_column(String(255), nullable=True)
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    height: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    birthday: Mapped[date] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(255), nullable=True)
    blood_type: Mapped[str] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[float] = mapped_column(nullable=True)
    # health_goal: Optional[HealthGoal]  # 선택적으로 사용자가 설정한 건강 목표
    # custom_health_goal: Optional[CustomHealthGoal]  # 사용자가 직접 입력한 목표

    # # 선택지 검증: 입력 값이 주어진 선택지 중 하나인지 확인
    # @validator('health_goal', pre=True)
    # def validate_health_goal(cls, v):
    #     allowed_goals = ["근력강화", "건강유지", "체중감량", "아직 목표가 없어요", "직접 입력할래요"]
    #     if v not in allowed_goals and v != "직접 입력할래요":
    #         raise ValueError("Invalid health goal")
    #     return v
