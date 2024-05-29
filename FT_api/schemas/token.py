from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None


class JWTCreate(BaseModel):
    access_token: str | None = None
    refresh_token: str | None = None


class JWTResp(BaseModel):
    access_token: str = Field(
        ..., serialization_alias="accessToken", title="Access Token", description="JWT Access Token"
    )
