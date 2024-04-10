from fastapi import APIRouter

from FT_api.api.endpoints.login import naver
from FT_api.api.endpoints.login import kakao

login_router = APIRouter()
login_router.include_router(kakao.router, prefix='/kakao')
login_router.include_router(naver.router)
