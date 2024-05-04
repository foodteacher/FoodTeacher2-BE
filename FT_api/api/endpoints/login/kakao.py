import requests

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.db.session import get_db
from FT_api.schemas.user import UserCreate, UserUpdate
from FT_api.crud.user import crud_user
from FT_api.core.security import create_jwt_access_and_refresh_tokens
from FT_api.crud.user import crud_user


router = APIRouter()
settings = get_setting()
ENV = settings.ENV
kakao_redirect_uri = KAKAO_REDIRECT_URI = (
    "http://localhost:8000/login/kakao/auth/callback"
    if ENV == "development"
    else "https://api2.foodteacher.xyz/login/kakao/auth/callback"
)
REST_API_KEY = settings.KAKAO_REST_API_KEY


# 엑세스 토큰을 저장할 변수
@router.get("/auth/callback",)
def kakao_auth(
    code: str,
    state: str | None,
    db: Session = Depends(get_db),
):

    kakao_token = get_kakao_token(code)

    kakao_access_token = kakao_token.get("access_token")
    kakao_refresh_token = kakao_token.get("refresh_token")

    kakao_id = get_kakao_id(kakao_access_token)
    user = crud_user.get_by_social_id(db, social_id=kakao_id)

    jwt = create_jwt_access_and_refresh_tokens(social_id=kakao_id)  
    url = f'http://v2.foodteacher.xyz/auth?accessToken={jwt.access_token}'
    if state == 'dev':
        url = f'http://localhost:3000/auth?accessToken={jwt.access_token}'


    if not user:
        new_user = UserCreate(
            user_id=kakao_id,
            provider="Kakao",
            access_token=kakao_access_token,
            refresh_token=kakao_refresh_token,
        )
        crud_user.create(db, obj_in=new_user)


        return RedirectResponse(url=url)

    update_data = UserUpdate(refresh_token=jwt.refresh_token)
    crud_user.update(db, db_obj=user, obj_in=update_data)

    return RedirectResponse(url=url)


def get_kakao_token(code):
    _url = f"https://kauth.kakao.com/oauth/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "grant_type": "authorization_code",
        "client_id": REST_API_KEY,
        "code": code,
        "redirect_uri": kakao_redirect_uri,
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
