import httpx
from bot.core.config import settings
from bot.core.constants import GROQ_AUDIO_URL
from bot.core.exceptions import NetworkException, BadResponseException, LLMException
from bot.helpers import get_header_for_ai

async def get_voice_text(file_path: str) -> str:
    headers = get_header_for_ai(settings.GROQ_API_KEY)
    try:
        async with httpx.AsyncClient() as client:
            with open(file_path, "rb") as audio_file:
                files = {"file": (file_path.split("/")[-1], audio_file, "audio/ogg")}
                data = {
                    "model": "whisper-large-v3",
                    "response_format": "json"
                }
                
                response = await client.post(
                    GROQ_AUDIO_URL, 
                    headers=headers, 
                    files=files, 
                    data=data, 
                    timeout=30.0
                )
                
        if response.status_code != 200:
            raise LLMException(f"Cloud STT Error: Server returned {response.status_code}")
            
        text = response.json().get("text", "").strip()
        if not text:
            raise BadResponseException("The audio is empty or no speech was recognized.")
            
        return text

    except httpx.RequestError as e:
        raise NetworkException(f"Network error while connecting to Groq: {str(e)}")
    except Exception as e:
        if isinstance(e, (NetworkException, BadResponseException, LLMException)):
            raise e
        raise LLMException(f"Unexpected error: {str(e)}")