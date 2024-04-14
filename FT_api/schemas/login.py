from pydantic import BaseModel

class NaverAuth(BaseModel):
    code: str
    state: str
