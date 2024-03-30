from fastapi import APIRouter

from FT_api.api.endpoints.user import user_info

user_router = APIRouter()
user_router.include_router(user_info.router, prefix="/user-info")
