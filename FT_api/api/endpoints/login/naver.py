from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_and_refresh_tokens
from FT_api.db.session import get_db
from FT_api.schemas.token import JWTResp
from FT_api.schemas.login import NaverAuth
from FT_api.schemas.user import UserCreate
from FT_api.crud.user import crud_user

import requests

router = APIRouter()
settings = get_setting()


# 엑세스 토큰을 저장할 변수
@router.post("/naver")
async def naver_auth(authorization: NaverAuth, x_environment: str = Header(None, alias="X-Environment"), db: Session = Depends(get_db)):
    naver_token = get_naver_token(authorization=authorization)
    naver_access_token = naver_token.get("access_token")
    naver_refresh_token = naver_token.get("refresh_token")

    naver_id = get_naver_id(naver_access_token)
    jwt = create_jwt_access_and_refresh_tokens(db=db, social_id=naver_id)

    new_user = UserCreate(
        user_id=naver_id,
        provider="Naver",
        access_token=naver_access_token,
        refresh_token=naver_refresh_token,
        jwt_refresh_token=jwt.refresh_token,
    )
    crud_user.create(db, obj_in=new_user)

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
        samesite='none' if x_environment != 'dev' else 'lax',
        secure=x_environment != 'dev'
    )

    return response


def get_naver_token(authorization: NaverAuth):
    naver_client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_SECRET

    _url = "https://nid.naver.com/oauth2.0/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "authorization_code",
        "client_id": naver_client_id,
        "client_secret": client_secret,
        "code": authorization.code,
        "state": authorization.state,
    }
    _res = requests.post(_url, headers=headers, data=data)

    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="naver code authentication failed"
            )


def get_naver_id(naver_access_token):
    headers = {
        "Authorization": f"Bearer {naver_access_token}"
    } 
    url = "https://openapi.naver.com/v1/nid/me"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        response_naver = response.json()
        return response_naver.get("response").get("id")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="naver access token authentication failed"
            )
