from pydantic import BaseModel

class AuthCode(BaseModel):
    code: str

class KakaoAuth(AuthCode):
    pass

class NaverAuth(AuthCode):
    state: str
