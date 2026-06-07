import httpx
from bot.config import settings
from bot.helpers import get_payload_for_ai
from bot.constants import AITask


HEADERS = {
    "Authorization": f"Bearer {settings.LLAMA_API_KEY}",
}




async def get_ai_answer(raw_text: str, task: AITask) -> str:
    if not raw_text or (len(raw_text.strip()) < 10 and task.name == 'SUMMARIZE'):
        return "The text is too short."

    payload = get_payload_for_ai(system_prompt=task.value, user_text=raw_text)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.LLAMA_URL, headers=HEADERS, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: Server returned {response.status_code}"
    except Exception as e:
        return "An error occurred while generating the response."