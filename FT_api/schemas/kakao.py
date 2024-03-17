from typing import Optional
from pydantic import BaseModel

class KakaoCode(BaseModel):
    code: str