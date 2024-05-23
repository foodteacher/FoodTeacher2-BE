from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from FT_api.api.urls import api_router

FT_api = FastAPI()

origins = [
    "http://localhost:3000",
    "https://v2.foodteacher.xyz",
]
FT_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

FT_api.include_router(api_router)


@FT_api.get("/")
def read_root():
    return "hello, 팩트폭행단~!"


from sqlalchemy.orm import Session
from FT_api.db.session import get_db
from fastapi import Depends
from typing import List
from pydantic import BaseModel
# from FT_api.models.user import (
#     SurveyQuestion,
#     SurveyResponse,
#     Option,
#     PastMedicine,
#     CurrentMedicine,
#     ReasonMedicine,
# )


# class Option_list(BaseModel):
#     text: str
#     order: int


# @FT_api.post("/add_survey")
# def add_survey(
#     question_text: str,
#     options_list: List[Option_list],
#     db: Session = Depends(get_db),
# ):

#     # Add SurveyQuestion
#     survey_question = SurveyQuestion(text=question_text, order=7)
#     db.add(survey_question)
#     db.commit()
#     db.refresh(survey_question)

#     # Add Options
#     options = []
#     for option in options_list:
#         new_option = Option(survey_question_id=survey_question.id, text=option.text, order=option.order)
#         db.add(new_option)
#         options.append(new_option)

#     db.commit()
#     for option in options:
#         db.refresh(option)

#     return {
#         "survey_question": survey_question,
#         "options": options,
#     }
