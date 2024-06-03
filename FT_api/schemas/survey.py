from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class SurveysRespSchema(BaseModel):
    id: int = Field(
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
    text: Optional[str] = Field(
        None,
        title="Text",
        description="문항",
        example="꽁꽁 얼어붙은 한강 위로 고양이가 거어다닙니다.",
    )
    selected: Optional[bool] = Field(
        None, title="Selected", description="문항 선택 여부", example=True
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
    option_id_list: Optional[List[int]] = Field(
        None,
        validation_alias="optionIdList",
        title="Option ID List",
        description="선택된 옵션 ID 목록",
        examples=[1, 2, 3],
    )
    text_answer: Optional[Dict[str, str | int]] = Field(
        None,
        validation_alias="textAnswer",
        title="Text Answer",
        description="텍스트 응답 (질문 ID와 응답 텍스트의 매핑, '직접 입력할래요'의 경우)",
        example={"optionId": 1, "answer": "answer1"},
    )


class QuestionReadRespSchema(QuestionRespSchema):
    total_page: int = Field(
        ...,
        serialization_alias="totalPage",
        title="Total Page",
        description="총 페이지 수",
        example=6
    )
    pass


# class SurveyCreateReqSchema(BaseModel):
#     title: Optional[str]
