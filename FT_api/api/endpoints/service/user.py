from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session, joinedload

from typing import List

from FT_api.core.config import get_setting
from FT_api.models.user import User
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user
from FT_api.schemas.user import (
    UserResp,
    UserUpdateReq,
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



