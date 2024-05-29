from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer

from sqlalchemy.orm import Session

from jose import jwt
from pydantic import ValidationError

from FT_api.core.config import get_setting
from FT_api.models.user import User
from FT_api.crud.user import crud_user
from FT_api.schemas.token import TokenPayload
from FT_api.db.session import get_db
from FT_api.core.security import create_jwt_access_token


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


class AuthRequired(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized user cannot access")

        token_type, token = auth_header.split(" ")

        if token_type != "Bearer":
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid token type")

        try:
            return token
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid token")


def decode_expried_jwt(token) -> TokenPayload:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY, algorithms=[settings.ALGORITHM],
            options={"verify_exp": False},
        )
        token_data = TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="error occured while decoding jwt",
        )
    
    return token_data

def get_current_user(db: Session = Depends(get_db), token: str = Depends(AuthRequired())) -> User:
    token_data = decode_jwt(token)

    user = crud_user.get_by_social_id(db, social_id=token_data.sub)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
            )
    
    return user
        

