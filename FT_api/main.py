from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from FT_api.db.session import Base, engine
from FT_api.api.api import api_router


# app 생성
# def create_tables():
#     Base.metadata.create_all(bind=engine)

# def get_application():
#     FT_api = FastAPI()
#     create_tables()
#     return FT_api

FT_api = FastAPI()

origins = [
    "http://localhost:3000",
    "https://foodteacher.xyz",
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
    return "hello, 팩트폭행단~!"