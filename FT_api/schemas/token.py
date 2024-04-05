from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class JWTCreate(BaseModel):
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None

class JWTResp(BaseModel):
    accessToken: Optional[str] = None
