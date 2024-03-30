from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_token
from FT_api.db.session import get_db
from FT_api.schemas.token import RefreshToken
from FT_api.api.depends import get_refresh_token, decode_jwt
from datetime import datetime


router = APIRouter()
settings = get_setting()


@router.post("/access_token")
def get_jwt_access_token(refresh_token: RefreshToken = Depends(get_refresh_token), db: Session = Depends(get_db)):
    token_data = decode_jwt(refresh_token.token)
    exp = token_data.exp
    if datetime.fromtimestamp(exp) > datetime.now():
        return RefreshToken(token=create_jwt_token(refresh_token.token))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token is expired. Please request access token"
        )
    
    
    