import httpx
from bot.config import settings

HEADERS = {
    "Authorization": f"Bearer {settings.LLAMA_API_KEY}",
}

async def summarize_text(raw_text: str) -> str:
    if not raw_text or len(raw_text.strip()) < 10:
        return "Текст слишком короткий для суммаризации."

    system_prompt = (
        "You are an expert text analyst. Your task is to create an ultra-concise, "
        "short summary of the provided text. Highlight only the absolute core points, "
        "agreements, or action items. Use a standard text bullet-point list (-). "
        "CRITICAL REQUIREMENTS:\n"
        "1. DO NOT use any emojis, stickers, or special visual symbols.\n"
        "2. The length of your summary must be AT LEAST 50% SHORTER than the original text. Cut all details.\n"
    )

    payload = {
        "messages": [
            {
                'role': 'system',
                'content': system_prompt
            },
            {
                'role': 'user',
                'content': raw_text
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.LLAMA_URL, headers=HEADERS, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"Error: Unable to connect to the summarization server (Status: {response.status_code})."
    except Exception as e:
        return "An error occurred while generating the summary."