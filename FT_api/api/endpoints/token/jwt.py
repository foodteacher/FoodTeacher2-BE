from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_token, create_jwt_refresh_token
from FT_api.schemas.token import JWTResp
from FT_api.api.depends import decode_expried_jwt, decode_jwt
from FT_api.crud.user import crud_user
from FT_api.db.session import get_db
from FT_api.api.depends import AuthRequired
from FT_api.core.redis import get_redis_client

router = APIRouter()
settings = get_setting()


@router.post("/access-token")
def get_jwt_access_token(
    access_token: str = Depends(AuthRequired()), db: Session = Depends(get_db), redis_client = Depends(get_redis_client)
):
    '''
    **유저가 access token이 만료되었을 때 새로운 access token 발급**
    '''
    access_token_data = decode_expried_jwt(access_token)
    access_token_sub = access_token_data.sub

    refresh_token = redis_client.get(f'jwt_refresh_token@{access_token_sub}')
    if refresh_token is None:
        raise HTTPException(status_code=404, detail="Refresh Token not found or expired")

    refresh_token_data = decode_jwt(refresh_token)

    if refresh_token_data.sub != access_token_sub:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="token data is not matched"
        )
    
    return JWTResp(access_token=create_jwt_access_token(access_token_sub))


@router.get("/test")
def get_test_token(db: Session = Depends(get_db)):
    return JWTResp(access_token=create_jwt_refresh_token(subject="3258042237"))

# @router.get("/user")
# def get_test_token_for_user(db: Session = Depends(get_db)):
#     user_obj = crud_user.get_by_social_id(db=db, social_id="3258042237")
#     new_data = UserUpdate(
#         jwt_refresh_token=create_jwt_refresh_token("3258042237")
#     )
#     crud_user.update(db=db, db_obj=user_obj, obj_in=new_data)
#     return Response(status_code=200)