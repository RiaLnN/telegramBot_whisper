import httpx
from config import settings

HEADERS = {"Authorization": f"Bearer {settings.HF_TOKEN}"}

async def enrich_text_with_emotions(raw_text: str) -> str:
    if not raw_text or len(raw_text.strip()) < 3:
        return raw_text

    system_prompt = (
        "Ты — текстовый редактор. Твоя задача — взять сырой, кривой текст из распознанного голосового сообщения, "
        "расставить знаки препинания, исправить грамматику и добавить эмоциональные маркеры в скобках, такие как: "
        "(вздох), (смеется), (кричит), (раздраженно), (неуверенно), если это понятно по контексту. "
        "Если человек ругается или кричит, выдели эти слова КАПСОМ. "
        "НЕ меняй смысл слов, НЕ пиши ничего от себя. Верни ТОЛЬКО итоговый обработанный текст без лишних вступлений."
    )

    prompt = f"<|system|>\n{system_prompt}</s>\n<|user|>\n{raw_text}</s>\n<|assistant|>\n"

    payload = {
        "messages": [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": raw_text
            }
        ],
        "model": "meta-llama/Llama-3.1-8B-Instruct:novita"
    }

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(settings.API_URL, headers=HEADERS, json=payload, timeout=30.0)
            
            if response.status_code == 200:
                result = response.json()
                generated_text = result["choices"][0]['message']['content']
                return generated_text.strip()
            
            elif response.status_code == 503:
                return raw_text
            else:
                return raw_text

    except Exception as e:
        return raw_text