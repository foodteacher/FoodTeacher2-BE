from fastapi import APIRouter

from FT_api.api.endpoints.user import mypage

user_router = APIRouter()
user_router.include_router(mypage.router, prefix="/mypage")
