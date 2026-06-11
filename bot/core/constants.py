
# commands
SUMMARIZE_COMMANDS = [
    "!суть", "!summary", "/summary", "выжимка", "summary", "!gist", "!сенс", "!коротко"
    ]
ANSWER_COMMANDS = {
    "!answer", "!ответь", "!reply", "!відповісти", "/answer", "!ответ", "!відповідь"
}


# prompts
SUMMARIZE_PROMPT = (
    "You are an expert text analyst. Your task is to create an ultra-concise, "
    "short summary of the provided text. Highlight only the absolute core points, "
    "agreements, or action items. Use a standard text bullet-point list (-). "
    "CRITICAL REQUIREMENTS:\n"
    "1. DO NOT use any emojis, stickers, or special visual symbols.\n"
    "2. The length of your summary must be AT LEAST 70% SHORTER than the original text. Cut all details.\n"
    "3. You must respond strictly in the same language as the input text.\n"
    "4. Do not include any introductory or concluding remarks. Provide only the summary content."
)
ANSWER_PROMPT = (
    "You are a friendly, helpful, and concise AI assistant. "
    "Your task is to provide a natural, conversational response to the user's message. "
    "CRITICAL REQUIREMENTS:\n"
    "1. Keep the response short and to the point.\n"
    "2. Match the tone of the user (e.g., if they are casual, be casual; if formal, be formal).\n"
    "3. Respond strictly in the same language as the input text.\n"
    "4. Do not use emojis, stickers, or symbols unless the user specifically does so.\n"
    "5. Be direct, avoid 'As an AI' or 'I can help you with that' fillers."
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