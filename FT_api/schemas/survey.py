from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Dict


class SurveysRespSchema(BaseModel):
    survey_id: int = Field(
        ...,
        serialization_alias="surveyId",
        title="Survey ID",
        description="설문 ID",
        example=1,
    )
    title: str = Field(..., title="Title", description="설문 제목", example="기본 설문")


class OptionRespSchema(BaseModel):
    option_id: int = Field(
        ...,
        serialization_alias="optionId",
        title="Option ID",
        description="문항 ID",
        example=1,
    )
    text: str = Field(
        None,
        title="Text",
        description="문항",
        example="꽁꽁 얼어붙은 한강 위로 고양이가 거어다닙니다.",
    )
    selected: bool = Field(
        None, title="Selected", description="문항 선택 여부", example=True
    )
    next_question_id: Optional[int] = Field(
        None,
        serialization_alias="nextQuesionId",
        title="Next Question ID",
        description="현재 문항 선택에 따른 다음 문제 ID",
        example=2,
    )


class QuestionRespSchema(BaseModel):
    question_id: int = Field(
        ...,
        serialization_alias="questionId",
        title="Question ID",
        description="문제 ID",
        example=1,
    )
    text: str = Field(
        ..., title="Text", description="문제", example="다음 중 기자가 한 말은?"
    )
    page_number: int = Field(
        ...,
        serialization_alias="pageNumber",
        title="Page Number",
        description="문제가 있는 페이지",
        example=3,
    )
    options: List[OptionRespSchema]


class SurveyRespSchema(BaseModel):
    survey_id: int = Field(
        ...,
        serialization_alias="surveyId",
        title="Survey ID",
        description="설문 ID",
        example=1,
    )
    title: str = Field(..., title="Title", description="설문 제목", example="기본 설문")
    questions: List[QuestionRespSchema]


class SurveyAnswerReqSchema(BaseModel):
    question_id: int = Field(
        ...,
        validation_alias="questionId",
        title="Question ID",
        description="문제 ID",
        example=1,
    )
    option_id_list: List[int] = Field(
        None,
        validation_alias="optionIdList",
        title="Option ID List",
        description="선택된 옵션 ID 목록",
        examples=[1, 2, 3],
    )
    text_answer: Dict[str, str | int] = Field(
        None,
        validation_alias="textAnswer",
        title="Text Answer",
        description="텍스트 응답 (질문 ID와 응답 텍스트의 매핑, '직접 입력할래요'의 경우)",
        example={"optionId": 1, "answer": "answer1"},
    )
