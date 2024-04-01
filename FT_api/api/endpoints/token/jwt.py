from fastapi import APIRouter, Depends, HTTPException, status

from FT_api.core.config import get_setting
from FT_api.core.security import create_jwt_token
from FT_api.db.session import get_db
from FT_api.schemas.token import JWTToken
from FT_api.api.depends import get_refresh_token, decode_jwt
from datetime import datetime, timezone


router = APIRouter()
settings = get_setting()


@router.post("/access-token")
def get_jwt_access_token(refresh_token: str = Depends(get_refresh_token)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST
        )
    token_data = decode_jwt(refresh_token)
    exp = token_data.exp
    if exp is not None or datetime.fromtimestamp(exp, tz=timezone.utc) > datetime.now(tz=timezone.utc):
        return JWTToken(accessToken=create_jwt_token(refresh_token))
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token is expired. Please request access token"
        )
    
    
    