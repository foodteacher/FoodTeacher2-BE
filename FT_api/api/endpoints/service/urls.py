from fastapi import APIRouter

from FT_api.api.endpoints.service import user
from FT_api.api.endpoints.service import voice
from FT_api.api.endpoints.service import survey

service_router = APIRouter()
service_router.include_router(user.router, prefix="/user", tags=["user"])
service_router.include_router(voice.router, prefix="/voice", tags=["voice"])
service_router.include_router(survey.router, prefix="/survey", tags=["survey"])
