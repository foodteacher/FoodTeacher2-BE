from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class JWTToken(BaseModel):
    accessToken: Optional[str] = None
    refreshToken: Optional[str] = None
    tokenType: Optional[str] = None