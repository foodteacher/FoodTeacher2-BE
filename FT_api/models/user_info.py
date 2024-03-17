from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List, Optional
from datetime import datetime

from FT_api.db.session import Base

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True, nullable=False, autoincrement=True)
    kakao_id: Mapped[str] = mapped_column(String(255))
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    height: Mapped[float] = mapped_column(nullable=True)
    weight: Mapped[float] = mapped_column(nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    gender: Mapped[str] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[float] = mapped_column(nullable=True)
    kakao_access_token: Mapped[str] = mapped_column(String(255))
    kakao_refresh_token: Mapped[str] = mapped_column(String(255))
    jwt_refresh_token: Mapped[str] = mapped_column(String(255))
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="user")


class UserDietPlanInfo(Base):
    __tablename__ = 'user_diet_plan_info'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), comment='Auto Increment')
    created_at: Mapped[datetime] = mapped_column(nullable=True)
    advice: Mapped[str] = mapped_column(String(255), nullable=True)
    recommanded_exercise: Mapped[str] = mapped_column(String(255), nullable=True)
    excess_calories: Mapped[float] = mapped_column(nullable=True)
    user: Mapped["User"] = relationship(back_populates="user_diet_plan_info")
    menus: Mapped[List["Menu"]] = relationship(back_populates="user_diet_plan_info")
    exercise: Mapped[List["Exercise"]] = relationship(back_populates="user_diet_plan_info")


class Menu(Base):
    __tablename__ = 'menu'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    name: Mapped[str] = mapped_column(String(255), nullable=True)
    calories: Mapped[float] = mapped_column(nullable=True)
    car: Mapped[float] = mapped_column(nullable=True)
    pro: Mapped[float] = mapped_column(nullable=True)
    fat: Mapped[float] = mapped_column(nullable=True)
    meal_time: Mapped[str] = mapped_column(String(255), nullable=True)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="menus")


class Exercise(Base):
    __tablename__ = 'exercise'
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, comment='Auto Increment')
    user_diet_plan_info_id: Mapped[int] = mapped_column(ForeignKey('user_diet_plan_info.id'), comment='Auto Increment')
    my_exercise: Mapped[str] = mapped_column(String(255), nullable=True)
    my_exercise_calories: Mapped[float] = mapped_column(nullable=True)
    user_diet_plan_info: Mapped["UserDietPlanInfo"] = relationship(back_populates="exercise")