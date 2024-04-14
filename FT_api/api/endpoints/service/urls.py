from fastapi import APIRouter

from FT_api.api.endpoints.service import user

service_router = APIRouter()
service_router.include_router(user.router, prefix="/user", tags=["user"])
