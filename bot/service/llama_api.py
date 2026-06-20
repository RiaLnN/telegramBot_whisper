import httpx
import logging
from bot.core.config import settings
from bot.helpers import get_payload_for_ai, get_header_for_ai
from bot.core.constants import AITask, LLAMA_URL
from bot.core.exceptions import NetworkException, BadResponseException, LLMException

logger = logging.getLogger(__name__)

async def get_ai_answer(raw_text: str, task: AITask) -> str:
    headers = get_header_for_ai(settings.LLAMA_API_KEY)
    if not raw_text or (len(raw_text.strip()) < 10 and task.name == 'SUMMARIZE'):
        raise BadResponseException("The text is too short to summarize.")

    payload = get_payload_for_ai(system_prompt=task.value, user_text=raw_text)

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(LLAMA_URL, headers=headers, json=payload, timeout=30.0)
            
            if response.status_code != 200:
                raise LLMException(f"Llama API Error: Server returned {response.status_code}")
                
            result = response.json()
            return result['choices'][0]['message']['content']

    except httpx.RequestError as e:
        logger.error(f"Llama API request network failure: {e}")
        raise NetworkException(f"Network error while connecting to Llama: {str(e)}")
    except Exception as e:
        if isinstance(e, (NetworkException, BadResponseException, LLMException)):
            raise e
        logger.error(f"Unexpected exception inside get_ai_answer: {e}")
        raise LLMException(f"Unexpected error generating response: {str(e)}")