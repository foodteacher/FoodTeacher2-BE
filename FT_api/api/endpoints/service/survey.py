from fastapi import APIRouter, Depends, HTTPException, Response, Body, Query

from sqlalchemy.orm import Session

from typing import List

from FT_api.models.user import User, Survey, Question, UserAnswers, Option
from FT_api.schemas.survey import (
    SurveysRespSchema,
    OptionRespSchema,
    QuestionRespSchema,
    SurveyRespSchema,
    SurveyAnswerReqSchema,
    QuestionReadRespSchema,
)
from FT_api.core.config import get_setting
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user


router = APIRouter()
settings = get_setting()


@router.get("/all", response_model=List[SurveysRespSchema])
def get_surveys(db: Session = Depends(get_db)):
    """
    **모든 설문 조회**
    """
    surveys = db.query(Survey).all()
    return surveys


@router.get("/{survey_id}", response_model=SurveyRespSchema)
def get_survey(
    survey_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    **현재 유저가 진행할 특정 설문 조회**
    """
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    questions = db.query(Question).filter(Question.survey_id == survey_id).all()
    answers = (
        db.query(UserAnswers)
        .filter(
            UserAnswers.user_id == current_user.id, UserAnswers.survey_id == survey_id
        )
        .all()
    )

    answer_dict = {answer.option_id: answer for answer in answers}

    questions_resp = [
        QuestionRespSchema(
            question_id=question.id,
            text=question.text,
            page_number=question.page_number,
            options=[
                OptionRespSchema(
                    option_id=option.id,
                    text=option.text,
                    selected=option.id in answer_dict,
                    next_question_id=option.next_question_id,
                )
                for option in question.options
            ],
        )
        for question in questions
    ]

    survey_resp = SurveyRespSchema(
        survey_id=survey.id, title=survey.title, questions=questions_resp
    )

    return survey_resp


@router.post("/{survey_id}/answers")
def save_answers(
    survey_id: int,
    user_answers: List[SurveyAnswerReqSchema] = Body(
        ...,
        example=[
            {
                "questionId": 1,
                "optionIdList": [1],
            },
            {
                "questionId": 2,
                "optionIdList": [7, 10],
            },
            {
                "questionId": 3,
                "optionIdList": [],
                "textAnswer": {"optionId": 1, "answer": "answer1"},
            },
            {
                "questionId": 4,
                "optionIdList": [22, 25],
                "textAnswer": {"optionId": 4, "answer": "answer2"},
            },
        ],
    ),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    **유저의 설문 답변을 저장**
    # textAnswer는 "직접 입력할래요"의 답변을 저장
    """
    for user_answer in user_answers:
        db_user_answers = (
            db.query(UserAnswers)
            .filter_by(
                user_id=current_user.id,
                survey_id=survey_id,
                question_id=user_answer.question_id,
            )
            .all()
        )

        # 기존 응답 삭제
        for db_user_answer in db_user_answers:
            db.delete(db_user_answer)
        db.commit()

        # 새로운 응답 생성
        for option_id in user_answer.option_id_list:
            new_answer = UserAnswers(
                user_id=current_user.id,
                survey_id=survey_id,
                question_id=user_answer.question_id,
                option_id=option_id,
                type=(
                    1 if len(user_answer.option_id_list) > 1 else 0
                ),  # 여러 개의 응답인지 확인
                answer=db.query(Option).filter_by(id=option_id).first().text,
            )
            db.add(new_answer)

        if user_answer.text_answer:
            new_answer = UserAnswers(
                user_id=current_user.id,
                survey_id=survey_id,
                question_id=user_answer.question_id,
                option_id=user_answer.text_answer.get("optionId"),
                answer=user_answer.text_answer.get("answer", ""),
                type=(
                    2 if not user_answer.question_id == 8 else 3
                ),  # '직접 입력할래요' 유형으로 설정
            )
            db.add(new_answer)

    db.commit()
    return Response(content="success")


@router.get("/question/", response_model=QuestionReadRespSchema)
def get_question(
    survey_id: int = Query(..., alias="surveyId"),
    question_id: int = Query(..., alias="questionId"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    '''
    질문 특정 질문을 조회
    '''
    question = (
        db.query(Question)
        .filter_by(survey_id=survey_id, id=question_id)
        .first()
    )

    option_list = db.query(Option).filter_by(question_id=question_id).all()

    answers = (
        db.query(UserAnswers)
        .filter(
            UserAnswers.user_id == current_user.id, UserAnswers.survey_id == survey_id
        )
        .all()
    )

    answer_dict = {answer.option_id: answer for answer in answers}

    question_data = QuestionReadRespSchema(
        question_id=question.id,
        text=question.text,
        page_number=question.page_number,
        options=[
            OptionRespSchema(
                option_id=option.id,
                text=option.text,
                selected=option.id in answer_dict,
                next_question_id=option.next_question_id,
            )
            for option in option_list
        ],
    )

    return question_data


# @router.post("")
# def create_survey(serialized_data: SurveyCreateReqSchema):
#     return
