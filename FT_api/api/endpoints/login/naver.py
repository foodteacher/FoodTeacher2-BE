from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_access_and_refresh_tokens
from FT_api.db.session import get_db
from FT_api.schemas.user import UserCreate, UserUpdate
from FT_api.crud.user import crud_user

import requests

router = APIRouter()
settings = get_setting()


# 엑세스 토큰을 저장할 변수
@router.get("/auth/callback")
def naver_auth(
    code: str,
    state: str,
    db: Session = Depends(get_db),
):
    naver_token = get_naver_token(code, state)
    naver_access_token = naver_token.get("access_token")
    naver_refresh_token = naver_token.get("refresh_token")

    naver_id = get_naver_id(naver_access_token)
    user = crud_user.get_by_social_id(db, social_id=naver_id)

    if not user:
        new_user = UserCreate(
            user_id=naver_id,
            provider="Naver",
            access_token=naver_access_token,
            refresh_token=naver_refresh_token,
        )
        crud_user.create(db, obj_in=new_user)

    jwt = create_jwt_access_and_refresh_tokens(social_id=naver_id)
    update_data = UserUpdate(refresh_token=jwt.refresh_token)
    crud_user.update(db, db_obj=user, obj_in=update_data)

    url = f"http://v2.foodteacher.xyz/auth?accessToken={jwt.access_token}"
    if state == "dev":
        url = f"http://localhost:3000/auth?accessToken={jwt.access_token}"

    return RedirectResponse(url=url)


def get_naver_token(code: str, state: str):
    naver_client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_SECRET

    _url = "https://nid.naver.com/oauth2.0/token"

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    data = {
        "grant_type": "authorization_code",
        "client_id": naver_client_id,
        "client_secret": client_secret,
        "code": code,
        "state": state,
    }
    _res = requests.post(_url, headers=headers, data=data)

    if _res.status_code == 200:
        _result = _res.json()
        return _result
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="naver code authentication failed",
        )


def get_naver_id(naver_access_token):
    headers = {"Authorization": f"Bearer {naver_access_token}"}
    url = "https://openapi.naver.com/v1/nid/me"

    response = requests.get(url, headers=headers)
    print(response.status_code)
    print(response.content)
    if response.status_code == 200:
        response_naver = response.json()
        return response_naver.get("response").get("id")
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="naver access token authentication failed",
        )
