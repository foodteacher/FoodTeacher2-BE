from fastapi import APIRouter

from FT_api.api.endpoints.login.urls import login_router
from FT_api.api.endpoints.token.urls import token_router
from FT_api.api.endpoints.service.urls import service_router
from FT_api.api.endpoints.logout.kakao import kakao

api_router = APIRouter()
api_router.include_router(login_router, prefix="/login", tags=["login"])
api_router.include_router(token_router, prefix="/token", tags=["token"])
api_router.include_router(service_router)
api_router.include_router(kakao.router, tags=["logout"])

# @app.on_event("startup")
# async def on_app_start():
#     """before app starts"""
#     Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def on_app_shutdown():
#     """after app shutdown"""
#     print("bye~!")