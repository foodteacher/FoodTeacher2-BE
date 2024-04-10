from fastapi import APIRouter, Depends, HTTPException, status, Header, Response
from fastapi.responses import JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_and_refresh_tokens
from FT_api.db.session import get_db
from FT_api.schemas.token import JWTResp
from FT_api.schemas.login import KakaoAuth
from FT_api.schemas.user import UserCreate
from FT_api.crud.user import crud_user

import requests

router = APIRouter()
settings = get_setting()
ENV = settings.ENV
kakao_redirect_uri = KAKAO_REDIRECT_URI = (
        "http://localhost:8000/login/kakao/auth/callback"
        if ENV == "development"
        else "https://api2.foodteacher.xyz/login/kakao/auth/callback"
    )



@router.get("/auth")
def kakao_auth():
    REST_API_KEY = settings.KAKAO_REST_API_KEY
    url = "https://kauth.kakao.com/oauth/authorize"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": REST_API_KEY,
        "redirect_uri": kakao_redirect_uri,
        "response_type": "code",
    }
    requests.post(url, headers=headers, data=data)

    return Response(status_code=200)


# 엑세스 토큰을 저장할 변수
@router.get("auth/callback")
async def kakao_(
    auth: KakaoAuth,
    db: Session = Depends(get_db),
):
    kakao_token = get_kakao_token(auth=auth)
    print(kakao_token)
    return Response(status_code=200)
    kakao_access_token = kakao_token.get("access_token")
    kakao_refresh_token = kakao_token.get("refresh_token")

    kakao_id = get_kakao_id(kakao_access_token)
    user = crud_user.get_by_social_id(db, social_id=kakao_id)
    jwt = create_jwt_access_and_refresh_tokens(db=db, social_id=kakao_id)

    if not user:
        new_user = UserCreate(
            user_id=kakao_id,
            provider="Kakao",
            access_token=kakao_access_token,
            refresh_token=kakao_refresh_token,
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
        samesite="none" if x_environment != "dev" else "lax",
        secure=x_environment != "dev",
    )

    return response


def get_kakao_token(*, auth: KakaoAuth):
    REST_API_KEY = settings.KAKAO_REST_API_KEY
    REDIRECT_URI = kakao_redirect_uri

    _url = f"https://kauth.kakao.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "code": auth.authorization_code,
        "redirect_uri": REDIRECT_URI,
    }
    _res = requests.post(_url, headers=headers, data=data)

    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(status_code=401, detail="Kakao code authentication failed")


def get_kakao_id(kakao_access_token):
    _url = "https://kapi.kakao.com/v2/user/me"
    headers = {"Authorization": f"Bearer {kakao_access_token}"}

    _res = requests.get(_url, headers=headers)

    if _res.status_code == 200:
        response_data = _res.json()
        print("kakao resp: ", response_data)
        return str(response_data.get("id"))
    else:
        raise HTTPException(
            status_code=401, detail="Kakao access token authentication failed"
        )

