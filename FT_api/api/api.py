from fastapi import APIRouter

from FT_api.api.endpoints.login.kakao import kakao
from FT_api.api.endpoints.logout.kakao import kakao

api_router = APIRouter()
api_router.include_router(kakao.router, prefix="/login", tags=["login"])
api_router.include_router(kakao.router, tags=["logout"])

# @app.on_event("startup")
# async def on_app_start():
#     """before app starts"""
#     Base.metadata.create_all(bind=engine)

# @app.on_event("shutdown")
# async def on_app_shutdown():
#     """after app shutdown"""
#     print("bye~!")