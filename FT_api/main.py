from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from FT_api.api.urls import api_router
from FT_api.core.redis import r

FT_api = FastAPI()

origins = [
    "http://localhost:3000",
    "https://v2.foodteacher.xyz",
]
FT_api.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # 모든 HTTP 메서드를 허용하려면 "*"
    allow_headers=["*"],  # 모든 HTTP 헤더를 허용하려면 "*"
)

FT_api.include_router(api_router)


@FT_api.get("/")
def read_root():
    print("redis is ", r.ping())
    return "hello, 팩트폭행단~!"
