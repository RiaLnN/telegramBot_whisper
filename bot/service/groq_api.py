import httpx
from bot.core.config import settings
from bot.core.constants import GROQ_AUDIO_URL

async def get_voice_text(file_path: str) -> str:
    headers = {
        "Authorization": f"Bearer {settings.GROQ_API_KEY}"
    }
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
            
            if response.status_code == 200:
                text = response.json().get("text", "").strip()
                return text if text else "The audio is empty or no speech was recognized."
            else:
                return f"Cloud STT Error: Server returned status code {response.status_code}"
                    
    except Exception as e:
        return f"An error occurred while sending the audio to the cloud service."