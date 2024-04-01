from datetime import datetime, timedelta, timezone
from typing import Any, Union
from fastapi import Depends

from jose import jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from FT_api.db.session import get_db
from FT_api.core.config import get_setting
from FT_api.schemas.token import JWTToken

settings = get_setting()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_jwt_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    current_time_utc = datetime.now(timezone.utc)
    if expires_delta:
        expire = current_time_utc + expires_delta
    else:
        expire = current_time_utc + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def create_jwt_access_and_refresh_tokens(*, social_id: int, db: Session = Depends(get_db)) -> JWTToken:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_jwt_token(subject=social_id, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_jwt_token(subject=social_id, expires_delta=refresh_token_expires)
    res = JWTToken(accessToken=access_token, refreshToken=refresh_token, tokenType="Bearer")
    return res

# def get_access_token(*, social_id)