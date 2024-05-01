from pydantic import BaseModel

class TTSRequest(BaseModel):
    text: str
    speaker: str = "nara"
    volume: int = 0
    speed: int = 0
    pitch: int = 0