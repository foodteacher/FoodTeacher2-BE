from pydantic import BaseModel

class KakaoAuth(AuthCode):
    pass

class NaverAuth(BaseModel):
    code: str
    state: str
