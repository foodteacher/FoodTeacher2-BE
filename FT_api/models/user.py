from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, Date
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import Optional, List
from datetime import date
from FT_api.db.session import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_social_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    provider: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    social_access_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    social_refresh_token: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    height: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    birthday: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    gender: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    blood_type: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    target_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    answers: Mapped[List["UserAnswers"]] = relationship(
        "UserAnswers", back_populates="user"
    )


class Survey(Base):
    __tablename__ = "surveys"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)

    questions: Mapped[List["Question"]] = relationship(
        "Question", back_populates="survey"
    )
    answers: Mapped[List["UserAnswers"]] = relationship(
        "UserAnswers", back_populates="survey"
    )
    total_page: Mapped[int] = mapped_column(Integer, nullable=False)


class Question(Base):
    __tablename__ = "questions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    survey_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("surveys.id"), nullable=False
    )
    text: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    page_number: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    survey: Mapped["Survey"] = relationship("Survey", back_populates="questions")
    options: Mapped[List["Option"]] = relationship(
        "Option", back_populates="question", foreign_keys="[Option.question_id]"
    )
    answers: Mapped[List["UserAnswers"]] = relationship(
        "UserAnswers", back_populates="question"
    )


class Option(Base):
    __tablename__ = "options"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=False
    )
    text: Mapped[Optional[Text]] = mapped_column(Text, nullable=True)
    order: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    next_question_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=True
    )  # 다음 질문으로 연결

    question: Mapped["Question"] = relationship(
        "Question", back_populates="options", foreign_keys="[Option.question_id]"
    )
    next_question: Mapped[Optional["Question"]] = relationship(
        "Question", remote_side=[Question.id], foreign_keys="[Option.next_question_id]"
    )
    answers: Mapped[List["UserAnswers"]] = relationship(
        "UserAnswers", back_populates="option"
    )


class UserAnswers(Base):
    __tablename__ = "user_answers"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    survey_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("surveys.id"), nullable=False
    )
    question_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("questions.id"), nullable=True
    )
    option_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey("options.id"), nullable=True
    )
    """
    0: 답변 한개
    1: 답변 여러개
    2: 직접 입력할래요.
    3: 약복용 + 횟수
    """
    type: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    answer: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    user: Mapped["User"] = relationship("User", back_populates="answers")
    survey: Mapped["Survey"] = relationship("Survey", back_populates="answers")
    question: Mapped["Question"] = relationship("Question", back_populates="answers")
    option: Mapped[Optional["Option"]] = relationship(
        "Option", back_populates="answers"
    )
