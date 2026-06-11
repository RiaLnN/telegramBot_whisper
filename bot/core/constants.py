
# commands
SUMMARIZE_COMMANDS = [
    "!суть", "!summary", "/summary", "выжимка", "summary", "!gist", "!сенс", "!коротко"
    ]
ANSWER_COMMANDS = {
    "!answer", "!ответь", "!reply", "!відповісти", "/answer", "!ответ", "!відповідь"
}


# prompts
SUMMARIZE_PROMPT = (
    "You are a summarization engine. "
    "Return only a concise summary of the provided text. "
    "Rules: no preamble, no commentary, no 'Here is a summary' — just the summary itself. "
    "Keep it as short as possible while preserving all key facts. "
    "Use the same language as the input text."
)

ANSWER_PROMPT = (
    "You are a reply assistant. "
    "Given a message, write a clear and concise response to it. "
    "Rules: no preamble, no meta-commentary — just the reply itself. "
    "Match the tone and language of the original message. "
    "Be direct and to the point."
)


# texts
MSG_PROCESSING_SUMMARY = "Extracting key points..."
MSG_PROCESSING_ANSWER = "Creating answer..."
MSG_ERROR_SUMMARY = "Text cannot be summarized."
MSG_ERROR_ANSWER = "Text cannot be answered."

from enum import Enum
class AITask(Enum):
    SUMMARIZE = SUMMARIZE_PROMPT
    ANSWER = ANSWER_PROMPT


# ai_api
LLAMA_URL = 'https://router.huggingface.co/v1/chat/completions'
GROQ_AUDIO_URL = 'https://api.groq.com/openai/v1/audio/transcriptions'

# celery
BROKER='redis://redis:6379/0'

# message errors
ERROR_EMPTY_AUDIO = "Failed to recognize speech or the audio file is empty."
ERROR_EMPTY_AI_RESPONSE = "AI model returned an empty response."
ERROR_TELEGRAM_API = "An error occurred while formatting or sending the AI response."
ERROR_TEXT_RENDER = "Error rendering output text."

MAX_MESSAGE_LENGTH = 4096