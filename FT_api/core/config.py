from pydantic_settings import BaseSettings, SettingsConfigDict

# from functools import lru_cache


class Settings(BaseSettings):
    ENV: str

    # MySQL 설정 정보
    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_ROOT_PASSWORD: str
    MYSQL_DATABASE: str
    MYSQL_USER: str
    MYSQL_PASSWORD: str

    # JWT 설정 정보
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 7 days = 7 days
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1
    # REFRESH_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 14
    REFRESH_TOKEN_EXPIRE_MINUTES: int = 5

    # kakao 설정 정보
    KAKAO_REST_API_KEY: str

    # naver
    NAVER_CLIENT_ID: str
    NAVER_SECRET: str

    # chatGPT
    OPENAI_API_KEY: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


def get_setting():
    return Settings()
