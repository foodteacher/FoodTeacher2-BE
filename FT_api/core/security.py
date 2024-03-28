from datetime import datetime, timedelta
from typing import Any, Union
from fastapi import Depends

from jose import jwt
from passlib.context import CryptContext

from sqlalchemy.orm import Session
from FT_api.db.session import get_db
from FT_api.core.config import get_setting
from FT_api.schemas.token import Token

settings = get_setting()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_token(subject: Union[str, Any], expires_delta: timedelta = None) -> str:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def get_jwt(*, social_id: int, db: Session = Depends(get_db)) -> Token:
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_token(subject=social_id, expires_delta=access_token_expires)

    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_token(subject=social_id, expires_delta=refresh_token_expires)
    res = Token(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")
    return res
