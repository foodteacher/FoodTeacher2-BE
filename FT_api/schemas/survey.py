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
    is_custom: bool = Field(
        ..., serialization_alias="isCustom", title="Is Custom", description="직접 입력한 문항인지", example=True
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


class HealthInfoRespSchema(BaseModel):
    health_goal: str = Field(..., serialization_alias="healthGoal", title="Health Goal",
                             description="건강 목표")
    health_check_up_cycle: str = Field(..., serialization_alias="healthCheckUpCycle", title="Health Check-up Cycle", description="건강 검진 주기")
    smoking: str = Field(..., title="Smoking", description="흡연 여부")


class DiseaseInfoRespSchema(BaseModel):
    my_disease: str = Field(..., serialization_alias="myDisease", title="My Disease", description="나의 질병")
    direct_family_disease: str = Field(..., serialization_alias="directFamilyDisease", title="Direct Family Disease", description="직계 가족 질병")

class TakenMedicationInfoRespSchema(BaseModel):
    is_long_term: str = Field(..., serialization_alias="isLongTerm", title="Long-term", description="정기 복용 약 여부")
    reason: Optional[str] = Field(None, title="Reason", description="복용 이유 or 복용 중단 이유")
    detail: Optional[List[str]] = Field(None, title="Detail", description="약 이름, 한 주에 몇 번 복용")


class HealthIndexRespSchema(BaseModel):
    stress: str = Field(..., title="Stress", description="스트레스")
    health_management: str = Field(..., serialization_alias="healthManagement", title="Health Management", description="건강 관리")


class SurveyRegisterResultRespSchema(BaseModel):
    """
    건강 정보
    health info
        건강 목표
        health goal
        건강 검진 주기
        health check-up cycle
        흡연 여부
        Smoking
    질병 정보
    disease info
        나의 질병
        my disease
        직계 가족 질병
        direct family disease
    복용중인 약 정보
    taken medication info
        정기 복용 약 여부
        is long-term
        복용 이유
        reason
        약 이름, 한 주에 몇 번 복용
        detail
    건강 척도
    health index
        스트레스
        stress
        건강 관리
        health management
    """
    health_info: HealthInfoRespSchema = Field(..., serialization_alias="healthInfo", title="Health Info", description="건강 정보")
    disease_info: DiseaseInfoRespSchema = Field(..., serialization_alias="diseaseInfo", title="Disease Info", description="질병 정보")
    taken_medication_info: TakenMedicationInfoRespSchema = Field(..., serialization_alias="takenMendicationInfo", title="Taken Medication Info", description="복용중인 약 정보")
    health_index: HealthIndexRespSchema = Field(..., serialization_alias="healthIndex", title="Health Index", description="건강 척도")
