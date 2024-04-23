from fastapi import APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

from datetime import datetime, timezone

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_token, create_jwt_refresh_token
from FT_api.schemas.token import JWTResp
from FT_api.schemas.user import UserUpdate
from FT_api.api.depends import decode_expried_jwt, decode_jwt
from FT_api.api.depends import reusable_oauth2
from FT_api.crud.user import crud_user
from FT_api.db.session import get_db

router = APIRouter()
settings = get_setting()


@router.post("/access-token")
def get_jwt_access_token(
    access_token: str = Depends(reusable_oauth2), db: Session = Depends(get_db)
):
    print(access_token)
    ac_token_data = decode_expried_jwt(access_token)
    ac_sub = ac_token_data.sub
    print(ac_token_data)

    current_user = crud_user.get_by_social_id(db=db, social_id=ac_sub)
    refresh_token = current_user.refresh_token
    re_token_data = decode_jwt(refresh_token)
    print(re_token_data)

    if re_token_data.sub != ac_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="token data is not matched"
        )
    if datetime.fromtimestamp(re_token_data.exp, tz=timezone.utc) > datetime.now(
        tz=timezone.utc
    ):
        return JWTResp(accessToken=create_jwt_access_token(ac_sub))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token is expired.",
        )


@router.get("")
def get_test_token(db: Session = Depends(get_db)):
    return JWTResp(accessToken=create_jwt_access_token(subject="3258042237"))

@router.get("/user")
def get_test_token_for_user(db: Session = Depends(get_db)):
    user_obj = crud_user.get_by_social_id(db=db, social_id="3258042237")
    new_data = UserUpdate(
        jwt_refresh_token=create_jwt_refresh_token("3258042237")
    )
    crud_user.update(db=db, db_obj=user_obj, obj_in=new_data)
    return Response(status_code=200)