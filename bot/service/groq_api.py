import httpx
import logging
from bot.core.groq_manager import groq_key_manager
from bot.core.constants import GROQ_AUDIO_URL
from bot.core.exceptions import NetworkException, BadResponseException, LLMException
from bot.helpers import get_header_for_ai

logger = logging.getLogger(__name__)

async def get_voice_text(file_path: str) -> str:
    max_retries = 5
    
    for attempt in range(max_retries):
        api_key = groq_key_manager.get_key()
        if not api_key:
            raise LLMException("No active Groq API keys available.")
            
        headers = get_header_for_ai(api_key)
        
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
            
            if response.status_code == 429:
                logger.warning(f"Rate limit hit (429) on attempt {attempt + 1}. Rotating key...")
                groq_key_manager.ban_key(api_key)
                continue
                
            if response.status_code != 200:
                raise LLMException(f"Cloud STT Error: Server returned {response.status_code}")
                
            text = response.json().get("text", "").strip()
            if not text:
                raise BadResponseException("The audio is empty or no speech was recognized.")
                
            return text

        except httpx.RequestError as e:
            logger.error(f"Network error on attempt {attempt + 1}: {e}")
            if attempt == max_retries - 1:
                raise NetworkException(f"Network error while connecting to Groq: {str(e)}")
            continue
            
        except Exception as e:
            if isinstance(e, (BadResponseException, LLMException)):
                raise e
            raise LLMException(f"Unexpected error: {str(e)}")

    raise LLMException("Failed to process audio after multiple key rotation retries.")