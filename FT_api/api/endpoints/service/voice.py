import requests

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from FT_api.core.config import get_setting
from FT_api.schemas.voice import TTSRequest


router = APIRouter()
settings = get_setting()


@router.post("/tts")
def text_to_speech(request: TTSRequest):
    url = "https://naveropenapi.apigw.ntruss.com/tts-premium/v1/tts"
    headers = {
        "X-NCP-APIGW-API-KEY-ID": settings.NCP_CLIENT_ID,
        "X-NCP-APIGW-API-KEY": settings.NCP_CLIENT_SECRET
    }
    data = {
        "speaker": "nara",
        "volume": 0,
        "speed": 0,
        "pitch": 0,
        "format": "mp3",
        "text": request.text
    }
    response = requests.post(url, headers=headers, data=data, stream=True)

    if response.status_code == 200:
        return StreamingResponse(response.iter_content(4096), media_type="audio/mpeg")
    else:
        raise HTTPException(status_code=response.status_code, detail="Failed to get TTS data")