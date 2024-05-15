from datetime import date
from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from FT_api.db.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    access_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    jwt_refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    survey_responses: Mapped[List["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="user"
    )


class SurveyQuestion(Base):
    __tablename__ = "survey_questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    options: Mapped[List["Option"]] = relationship(
        "Option", back_populates="survey_question"
    )


class Option(Base):
    __tablename__ = "options"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    survey_question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("survey_questions.id"), nullable=False
    )
    text: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    survey_question: Mapped["SurveyQuestion"] = relationship(
        "SurveyQuestion", back_populates="options"
    )
    survey_responses: Mapped[List["SurveyResponse"]] = relationship(
        "SurveyResponse", back_populates="option"
    )


class SurveyResponse(Base):
    __tablename__ = "survey_response"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    option_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("options.id"), nullable=False
    )

    user: Mapped["User"] = relationship("User", back_populates="survey_responses")
    option: Mapped["Option"] = relationship("Option", back_populates="survey_responses")
    current_medicine: Mapped["CurrentMedicine"] = relationship(
        "CurrentMedicine", back_populates="survey_response"
    )
    past_medicine: Mapped["PastMedicine"] = relationship(
        "PastMedicine", back_populates="survey_response"
    )
    reason_medicine: Mapped["ReasonMedicine"] = relationship(
        "ReasonMedicine", back_populates="survey_response"
    )


class CurrentMedicine(Base):
    __tablename__ = "current_medicine"
    survey_response_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("survey_response.id"), primary_key=True
    )
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    frequency: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    survey_response: Mapped["SurveyResponse"] = relationship(
        "SurveyResponse", back_populates="current_medicine"
    )


class PastMedicine(Base):
    __tablename__ = "past_medicine"
    survey_response_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("survey_response.id"), primary_key=True
    )
    description: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    survey_response: Mapped["SurveyResponse"] = relationship(
        "SurveyResponse", back_populates="past_medicine"
    )


class ReasonMedicine(Base):
    __tablename__ = "reason_medicine"
    survey_response_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("survey_response.id"), primary_key=True
    )
    reason: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    survey_response: Mapped["SurveyResponse"] = relationship(
        "SurveyResponse", back_populates="reason_medicine"
    )
