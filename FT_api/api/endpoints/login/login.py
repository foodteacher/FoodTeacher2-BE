from fastapi import APIRouter

import kakao
import naver

login_router = APIRouter()
login_router.include_router(kakao.router)
login_router.include_router(naver.router)
