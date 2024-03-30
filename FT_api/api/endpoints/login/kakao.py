from fastapi import APIRouter, Depends, HTTPException, Request, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_and_refresh_tokens
from FT_api.db.session import get_db
from FT_api.schemas.token import Token
from FT_api.schemas.login import KakaoAuth
from FT_api.schemas.user import UserUpdate, UserCreate
from FT_api.crud.user import crud_user

import requests

router = APIRouter()
settings = get_setting()

# 엑세스 토큰을 저장할 변수
@router.post('/kakao')
async def kakao_auth(authorization_code: KakaoAuth, x_environment: str = Header(None, alias="X-Environment"), db: Session = Depends(get_db)):
    print("x_environment는 ", x_environment, "입니다.")
    print("x_environment의 타입은 ", type(x_environment), "입니다.")
    kakao_token = get_kakao_token(authorization_code=authorization_code, x_environment=x_environment)
    kakao_access_token = kakao_token.get("access_token")
    kakao_refresh_token = kakao_token.get("refresh_token")

    kakao_id = get_kakao_id(kakao_access_token)
    user = crud_user.get_by_kakao_id(db, kakao_id=kakao_id)
    jwt = create_jwt_access_and_refresh_tokens(db=db, social_id=kakao_id)
    
    # 쿠키에 refresh_token 설정, SameSite=None 및 secure=True 추가
    response = JSONResponse(status_code=status.HTTP_200_OK, content={"access_token": jwt.access_token})
    if x_environment != 'dev':
        response.set_cookie(
            key="refresh_token",
            value=jwt.refresh_token,
            httponly=True,  # 클라이언트 사이드 스크립트에서 접근 불가능하도록 설정
            max_age=1800,  # 쿠키 유효 시간 (예: 1800초 = 30분)
            expires=1800,
            samesite='None',  # 다른 도메인 간 요청에서도 쿠키를 전송
            secure=True  # 쿠키가 HTTPS를 통해서만 전송되도록 설정
        )
    else:
        response.set_cookie(
            key="refresh_token",
            value=jwt.refresh_token,
            httponly=True,  # 클라이언트 사이드 스크립트에서 접근 불가능하도록 설정
            max_age=1800,  # 쿠키 유효 시간 (예: 1800초 = 30분)
            expires=1800,
            samesite='Lax',  # 다른 도메인 간 요청에서도 쿠키를 전송
            secure=False  # 쿠키가 HTTPS를 통해서만 전송되도록 설정
        )
    
    if user:
        return response
    else:
        new_user = UserCreate(
        user_id=kakao_id,
        provider="Kakao",
        access_token=kakao_access_token,
        refresh_token=kakao_refresh_token,
        jwt_refresh_token=jwt.refresh_token
    )
    crud_user.create(db, obj_in=new_user)

    return response

def get_kakao_token(*, authorization_code: KakaoAuth, x_environment: str):
    REST_API_KEY = settings.KAKAO_REST_API_KEY
    if x_environment != 'dev':
        REDIRECT_URI = settings.REDIRECT_URI_PRODUCTION
    else:
        REDIRECT_URI = settings.REDIRECT_URI_DEVELOPMENT
    
    # REDIRECT_URI = settings.REDIRECT_URI_DEVELOPMENT
    _url = f'https://kauth.kakao.com/oauth/token'
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "code": authorization_code.code,
        "redirect_uri": REDIRECT_URI
    }
    _res = requests.post(_url, headers=headers, data=data)
    
    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(status_code=401, detail="Kakao code authentication failed")

def get_kakao_id(kakao_access_token):
    _url = "https://kapi.kakao.com/v2/user/me"
    headers = {
        "Authorization": f"Bearer {kakao_access_token}"
    }

    _res = requests.get(_url, headers=headers)

    if _res.status_code == 200:
        response_data = _res.json()
        user_id = response_data.get("id")
        return user_id
    else:
        raise HTTPException(status_code=401, detail="Kakao access token authentication failed")

def create_user(*, db: Session, new_user: UserCreate):
    user = crud_user.create(db, obj_in=new_user)
    return user
