from pydantic import BaseModel

class AuthCode(BaseModel):
    authorization_code: str

class KakaoAuth(AuthCode):
    pass

class NaverAuth(AuthCode):
    state: str
