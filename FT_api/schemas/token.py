from pydantic import BaseModel

class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None

class JWTCreate(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None

class JWTResp(BaseModel):
    accessToken: str | None = None
