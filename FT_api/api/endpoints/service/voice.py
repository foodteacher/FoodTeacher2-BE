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
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    data = f"speaker={request.speaker}&volume={request.volume}&speed={request.speed}&pitch={request.pitch}&format=mp3&text={urllib.parse.quote(request.text)}"

    request = urllib.request.Request(url)
    request.add_header("X-NCP-APIGW-API-KEY-ID", settings.NCP_CLIENT_ID)
    request.add_header("X-NCP-APIGW-API-KEY", settings.NCP_CLIENT_SECRET)

    try:
        with urllib.request.urlopen(request, data=data.encode("utf-8")) as response:
            if response.getcode() == 200:
                return StreamingResponse(response, media_type="audio/mpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
