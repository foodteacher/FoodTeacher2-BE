from fastapi import APIRouter, Depends, Header, status
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.models.user_info import User
from FT_api.db.session import get_db
from FT_api.api.depends import get_current_user
from FT_api.schemas.user import UserInDBBase, UserUpdate
from FT_api.schemas.token import JWTResp
from FT_api.crud.user import crud_user
from FT_api.core.security import create_jwt_access_and_refresh_tokens


router = APIRouter()
settings = get_setting()


@router.get(
    "/info",
    # response_model=UserInDBBase,
    # responses={
    #     404: {"model": "UserInDBBase", "description": "The item was not found"},
    #     200: {
    #         "description": "Item requested by ID",
    #         "content": {
    #             "application/json": {
    #                 "example": {"id": "bar", "value": "The bar tenders"}
    #             }
    #         },
    #     },
    # },
)
def get_user_info(current_user: User = Depends(get_current_user)):
    return current_user


@router.patch("/regist")
def register_user(
    update_data: UserUpdate,
    x_environment: str = Header(None, alias="X-Environment"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    jwt = create_jwt_access_and_refresh_tokens(social_id=current_user.user_id)

    update_data.jwt_refresh_token = jwt.refresh_token
    crud_user.update(db, db_obj=current_user, obj_in=update_data)

    content = JWTResp(accessToken=jwt.access_token)
    # 쿠키에 refresh_token 설정, SameSite=None 및 secure=True 추가
    response = JSONResponse(
        status_code=status.HTTP_200_OK, content=content.model_dump()
    )
    response.set_cookie(
        key="refresh_token",
        value=jwt.refresh_token,
        httponly=True,
        max_age=1800,
        expires=1800,
        samesite="none" if x_environment != "dev" else "lax",
        secure=x_environment != "dev",
    )

    return response
