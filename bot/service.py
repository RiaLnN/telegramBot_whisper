import httpx
from config import settings

async def get_voice_text(file_path: str):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url=settings.WHISPER_URL, 
                json={'file_path': file_path},
                timeout=60.0 
            )
            if response.status_code == 200:
                return response.json().get("text", "Не удалось распознать текст."), True
            else:
                return f"Ошибка сервера Whisper: {response.status_code}", False
        
    except Exception as e:
        return "Произошла ошибка при обработке аудио.", False