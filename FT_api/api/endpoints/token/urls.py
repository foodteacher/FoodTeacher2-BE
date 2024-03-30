from fastapi import APIRouter

from FT_api.api.endpoints.token import jwt

token_router = APIRouter()
token_router.include_router(jwt.router, prefix="/jwt")
