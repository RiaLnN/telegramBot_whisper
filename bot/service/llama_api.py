import httpx
import logging
from bot.core.config import settings
from bot.helpers import get_payload_for_ai, get_header_for_ai
from bot.core.constants import AITask, LLAMA_URL, PROMPT_PRESETS
from bot.core.exceptions import NetworkException, BadResponseException, LLMException

logger = logging.getLogger(__name__)

async def get_ai_answer(raw_text: str, task: AITask, preset_key: str = "default") -> str:
    headers = get_header_for_ai(settings.LLAMA_API_KEY)
    
    if not raw_text or (len(raw_text.strip()) < 10 and task == AITask.SUMMARIZE):
        raise BadResponseException("The text is too short to summarize.")

    modifier = PROMPT_PRESETS.get(preset_key, PROMPT_PRESETS["default"])
    
    final_system_prompt = f"{task.value} {modifier}".strip()

    payload = get_payload_for_ai(system_prompt=final_system_prompt, user_text=raw_text)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(LLAMA_URL, headers=headers, json=payload, timeout=30.0)
            
            if response.status_code != 200:
                raise LLMException(f"Llama API Error: Server returned {response.status_code}")
                
            result = response.json()
            return result['choices'][0]['message']['content']

    except httpx.RequestError as e:
        logger.error(f"Llama network failure: {e}")
        raise NetworkException(f"Network error while connecting to Llama: {str(e)}")
    except Exception as e:
        if isinstance(e, (NetworkException, BadResponseException, LLMException)):
            raise e
        logger.error(f"Unexpected Llama error: {e}")
        raise LLMException(f"Unexpected error generating response: {str(e)}")