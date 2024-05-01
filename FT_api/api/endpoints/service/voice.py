from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from FT_api.core.config import get_setting
from FT_api.schemas.voice import TTSRequest

import urllib.request
import urllib.parse

router = APIRouter()
settings = get_setting()


@router.post("/tts")
def text_to_speech(request: TTSRequest):
    speaker: str = "nara"
    volume: int = 0
    speed: int = 0
    pitch: int = 0
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    data = f"speaker={speaker}&volume={volume}&speed={speed}&pitch={pitch}&format=mp3&text={urllib.parse.quote(request.text)}"

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", settings.NCP_CLIENT_ID)
    request.add_header("X-NCP-APIGW-API-KEY", settings.NCP_CLIENT_SECRET)

    try:
        with urllib.request.urlopen(request, data=data.encode("utf-8")) as response:
            if response.status == 200:
                def stream_generator():
                    while True:
                        chunk = response.read(4096)  # 4096 바이트씩 읽기
                        if not chunk:
                            break
                        yield chunk
                return StreamingResponse(stream_generator(), media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
