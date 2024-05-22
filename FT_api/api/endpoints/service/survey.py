from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from typing import List

from FT_api.models.user import Survey
from FT_api.schemas.survey import SurveysRespSchema
from FT_api.core.config import get_setting
from FT_api.db.session import get_db

router = APIRouter()
settings = get_setting()

@router.get("", response_model=List[SurveysRespSchema])
def get_surveys(db: Session = Depends(get_db)):
    surveys = db.query(Survey).all()
    return surveys  