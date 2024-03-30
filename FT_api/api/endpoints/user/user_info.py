from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.models.user_info import User
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user


router = APIRouter()
settings = get_setting()


@router.get("/")
def get_user_info(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return current_user
