import json

from fastapi import Depends, HTTPException, status, Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.models.user_info import User
from FT_api.crud.user import crud_user
from FT_api.schemas.token import TokenPayload
from datetime import datetime, timezone

from FT_api.db.session import get_db

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/")
settings = get_setting()

def decode_jwt(token) -> TokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token is expired"
    )
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="error occured while decoding jwt",
        )
    
    return token_data

def get_current_user(db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)) -> User:
    token_data = decode_jwt(token)

    user = crud_user.get_by_social_id(db, social_id=token_data.sub)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    return user
        


def get_refresh_token(refresh_token: str = Cookie(None)):
    return refresh_token