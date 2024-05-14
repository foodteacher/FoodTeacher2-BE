from pydantic import BaseModel, Field


class TTSRequest(BaseModel):
    text: str = Field(
        ...,
        title="Text",
        description="음성으로 변환할 텍스트",
        example="꽁꽁 얼어붙은 한강 위로 고양이가 걸어다닙니다.",
    )
