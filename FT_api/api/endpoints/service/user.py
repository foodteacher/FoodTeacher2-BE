from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload

from typing import List

from FT_api.core.config import get_setting
from FT_api.models.user import User, Survey, Question, UserResponse, Option
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user
from FT_api.schemas.user import (
    UserResp,
    UserUpdateReq,
    OptionRespSchema,
    QuestionRespSchema,
    SurveyRespSchema,
    UserRespSchema,
)
from FT_api.schemas.token import JWTResp
from FT_api.crud.user import crud_user
from FT_api.core.security import create_jwt_access_and_refresh_tokens


router = APIRouter()
settings = get_setting()


@router.get(
    "/info",
    response_model=UserResp,
)
def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/regist", response_model=JWTResp)
def register_user(
    update_data: UserUpdateReq,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    update_data = update_data.model_dump()
    jwt = create_jwt_access_and_refresh_tokens(social_id=current_user.user_social_id)

    update_data["jwt_refresh_token"] = jwt.refresh_token
    crud_user.update(db, db_obj=current_user, obj_in=update_data)

    content = JWTResp(accessToken=jwt.access_token)
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=content.model_dump()
    )

    return response


@router.get("/api/survey/{survey_id}", response_model=SurveyRespSchema)
def get_survey(
    survey_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    survey = db.query(Survey).filter(Survey.id == survey_id).first()
    if not survey:
        raise HTTPException(status_code=404, detail="Survey not found")

    questions = db.query(Question).filter(Question.survey_id == survey_id).all()
    responses = (
        db.query(UserResponse)
        .filter(
            UserResponse.user_id == current_user.id, UserResponse.survey_id == survey_id
        )
        .all()
    )

    response_dict = {response.option_id: response for response in responses}

    survey_data = {
        "id": survey.id,
        "title": survey.title,
        "description": survey.description,
        "questions": [],
    }

    for question in questions:
        question_data = {
            "id": question.id,
            "text": question.text,
            "page_number": question.page_number,
            "options": [
                {
                    "id": option.id,
                    "text": option.text,
                    "selected": option.id in response_dict,
                    "next_question_id": option.next_question_id,
                }
                for option in question.options
            ],
            "response": {
                "option_id": (
                    response_dict[question.id].option_id
                    if question.id in response_dict
                    else None
                ),
                "text_response": (
                    response_dict[question.id].response
                    if question.id in response_dict
                    else None
                ),
            },
        }
        survey_data["questions"].append(question_data)

    return survey_data


@router.post("/api/response")
def save_response(response: UserRespSchema, db: Session = Depends(get_db)):
    db_response = (
        db.query(UserResponse)
        .filter(
            UserResponse.user_id == response.user_id,
            UserResponse.survey_id == response.survey_id,
            UserResponse.question_id == response.question_id,
        )
        .first()
    )

    if db_response:
        db_response.option_id = response.option_id
        db_response.response = response.user_response
    else:
        db_response = UserResponse(
            user_id=response.user_id,
            survey_id=response.survey_id,
            question_id=response.question_id,
            option_id=response.option_id,
            response=response.response,
        )
        db.add(db_response)

    db.commit()

    next_question_id = None
    if response.option_id:
        option = db.query(Option).filter(Option.id == response.option_id).first()
        if option:
            next_question_id = option.next_question_id

    return {"status": "success", "next_question_id": next_question_id}
