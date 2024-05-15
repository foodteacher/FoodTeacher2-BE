from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from FT_api.db.session import get_db

from FT_api.core.config import get_setting
from FT_api.api.depends import get_current_user
from FT_api.crud.user import crud_user
from FT_api.models.user import User
from FT_api.schemas.user import UserRead

import requests


router = APIRouter()
settings = get_setting()

@router.post('/logout', response_model=UserRead, response_model_exclude={"kakao_access_token": True, "kakao_refresh_token": True, "jwt_refresh_token": True})
def logout(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)) -> UserRead:
    kakao_logout(current_user=current_user)
    crud_user.remove_field(db=db, db_obj=current_user, field="kakao_refresh_token")
    crud_user.remove_field(db=db, db_obj=current_user, field="kakao_access_token")
    res = crud_user.remove_field(db=db, db_obj=current_user, field="jwt_refresh_token")
    return res

def kakao_logout(current_user: User):
    access_token = current_user.kakao_access_token
    _url = f"https://kapi.kakao.com/v1/user/logout"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Bearer {access_token}"
    }
    _res = requests.post(_url, headers=headers)
    
    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(status_code=401, detail="Kakao logout failed")