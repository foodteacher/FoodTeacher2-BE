from typing import Optional
from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: Optional[str] = None
    exp: Optional[int] = None

class BaseToken(BaseModel):
    token: str

class RefreshToken(BaseToken):
    pass

class AccessToken(BaseToken):
    pass
