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
    SurveyRegisterResultRespSchema,
    HealthInfoRespSchema,
    DiseaseInfoRespSchema,
    TakenMedicationInfoRespSchema,
    HealthIndexRespSchema,
)
from FT_api.core.config import get_setting
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user


router = APIRouter()
settings = get_setting()


def get_survey_data(
    question_id_list: List[int], current_user: User, survey: Survey, db: Session
):
    res = []
    questions = db.query(Question).filter(Question.id.in_(question_id_list)).all()
    for question in questions:
        option_list = db.query(Option).filter_by(question_id=question.id).all()

        answers = (
            db.query(UserAnswers)
            .filter(
                UserAnswers.user_id == current_user.id,
                UserAnswers.survey_id == survey.id,
                UserAnswers.question_id.in_(question_id_list),
            )
            .all()
        )

        answer_dict = {answer.option_id: answer for answer in answers}

        res.append(
            QuestionReadRespSchema(
                question_id=question.id,
                text=question.text,
                total_page=survey.total_page,
                options=[
                    OptionRespSchema(
                        option_id=option.id,
                        text=option.text,
                        selected=option.id in answer_dict,
                    )
                    for option in option_list
                ],
            )
        )

    if len(question_id_list) == 1:
        return res
    if len(res) != len(question_id_list) - 1:
        return res[:-1]
    return res


@router.get("/register", response_model=List[QuestionReadRespSchema])
def get_registered_survey_by_page_num(
    page_num: int = Query(..., alias="pageNum"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    survey = db.query(Survey).filter_by(title="회원가입 설문").first()

    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    pre_page_num = page_num - 1

    pre_question = (
        db.query(Question)
        .filter_by(survey_id=survey.id, page_number=pre_page_num)
        .order_by(Question.order.desc())
        .first()
    )

    page_num_question_list = db.query(Question).filter_by(page_number=page_num).all()
    page_num_question_id_list = [q.id for q in page_num_question_list]

    if not pre_question:
        return get_survey_data(
            question_id_list=page_num_question_id_list,
            current_user=current_user,
            survey=survey,
            db=db,
        )

    pre_answer_list = (
        db.query(UserAnswers)
        .filter(
            UserAnswers.user_id == current_user.id,
            UserAnswers.survey_id == survey.id,
            UserAnswers.question_id.in_(
                db.query(Question.id).filter_by(page_number=pre_page_num)
            ),
        )
        .all()
    )

    current_page_answer_list = (
        db.query(UserAnswers)
        .filter(
            UserAnswers.user_id == current_user.id,
            UserAnswers.survey_id == survey.id,
            UserAnswers.question_id.in_(
                db.query(Question.id).filter_by(page_number=page_num)
            ),
        )
        .all()
    )

    pre_answer_dic = {answer.option_id: answer for answer in pre_answer_list}
    req_page_answer_dic = {
        answer.question_id: answer.option_id for answer in current_page_answer_list
    }

    start_question_id = None
    for option in pre_question.options:
        if option.id in pre_answer_dic:
            start_question_id = option.next_question_id
            break
    else:
        if not start_question_id:
            start_question_id = page_num_question_id_list[0]

    next_question_id_list = [start_question_id]
    next_question_id = start_question_id

    while next_question_id in page_num_question_id_list:
        if not req_page_answer_dic:
            next_question_id = (
                db.query(Question)
                .filter_by(id=next_question_id)
                .first()
                .options[0]
                .next_question_id
            )
        else:
            option_id = req_page_answer_dic[next_question_id]
            next_question_id = (
                db.query(Option).filter_by(id=option_id).first().next_question_id
            )

        next_question_id_list.append(next_question_id)
    return get_survey_data(
        question_id_list=next_question_id_list,
        current_user=current_user,
        survey=survey,
        db=db,
    )


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


@router.get("/register/result", response_model=SurveyRegisterResultRespSchema)
def get_register_survey_result(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """
    **회원가입 설문 결과 조회**
    """
    survey = db.query(Survey).filter_by(title="회원가입 설문").first()

    health_info = {}
    disease_info = {}
    taken_medication_info = {}
    health_index = {}
    for question_num in range(1, 12):
        user_answers = (
        db.query(UserAnswers)
        .filter_by(
            user_id=current_user.id,
            survey_id=survey.id,
            question_id=question_num,
        )
        .all()
    )
        if not user_answers:
            pass

        if question_num != 8:
            answer = ""
            for user_answer in user_answers:
                if not answer:
                    answer += user_answer.answer
                else:
                    answer += ", " + user_answer.answer
        else:
            answer_list = [user_answer.answer for user_answer in user_answers]

        if question_num == 1:
            health_info["health_goal"] = answer
            pass
        if question_num == 2:
            health_info["health_check_up_cycle"] = answer
            pass
        if question_num == 3:
            health_info["smoking"] = answer
            pass
        if question_num == 4:
            disease_info["my_disease"] = answer
            pass
        if question_num == 5:
            disease_info["direct_family_disease"] = answer
            pass
        if question_num == 6:
            taken_medication_info["is_long_term"] = user_answer.answer
            pass
        if question_num == 7:
            taken_medication_info["reason"] = answer
            pass
        if question_num == 8:
            taken_medication_info["detail"] = answer_list
            pass
        if question_num == 9:
            taken_medication_info["reason"] = answer
            pass
        if question_num == 10:
            health_index["stress"] = answer
            pass
        if question_num == 11:
            health_index["health_management"] = answer

    health_info = HealthInfoRespSchema(**health_info)
    disease_info = DiseaseInfoRespSchema(**disease_info)
    taken_medication_info = TakenMedicationInfoRespSchema(**taken_medication_info)
    health_index = HealthIndexRespSchema(**health_index)
    res = SurveyRegisterResultRespSchema(
        health_info=health_info,
        disease_info=disease_info,
        taken_medication_info=taken_medication_info,
        health_index=health_index,
    )
    return res


@router.post("/register/answers")
def save_register_survey_answers(
    user_answers: List[SurveyAnswerReqSchema] = Body(
        ...,
        example=[
            {
                "questionId": 1,
                "optionIdList": [1],
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
    survey = db.query(Survey).filter_by(title="회원가입 설문").first()
    survey_id = survey.id
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


@router.post("/{survey_id}/answers/")
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
