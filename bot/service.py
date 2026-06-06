import httpx
from config import settings


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
                    settings.GROQ_AUDIO_URL, 
                    headers=headers, 
                    files=files, 
                    data=data, 
                    timeout=30.0
                )
            
            if response.status_code == 200:
                text = response.json().get("text", "").strip()
                return text
            else:
                return f"Ошибка облачного STT: {response.status_code}"
                    
    except Exception as e:
        return "Произошла ошибка при отправке аудио в облако."