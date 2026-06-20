from enum import Enum
# commands
SUMMARIZE_COMMANDS = [
    "!суть", "!summary", "/summary", "выжимка", "summary", "!gist", "!сенс", "!коротко"
    ]
ANSWER_COMMANDS = {
    "!answer", "!ответь", "!reply", "!відповісти", "/answer", "!ответ", "!відповідь"
}
TRANSCRIBE_COMMANDS = {
    "!транскрипт", "!transcribe", "/transcribe", "!текст", "!розшифрувати", "!напиши"
}

# texts
MSG_PROCESSING_SUMMARY = "Extracting key points..."
MSG_PROCESSING_ANSWER = "Creating answer..."
MSG_ERROR_SUMMARY = "Text cannot be summarized."
MSG_ERROR_ANSWER = "Text cannot be answered."
MSG_PROCESSING_VOICE = "Transcribing voice message..."
MSG_ERROR_VOICE = "Internal systems error. Please try again later."
ERROR_UNEXPECTED = "An unexpected error occurred while processing the request."

# prompts
SUMMARIZE_BASE = (
    "You are a summarization engine. "
    "Return only a concise summary of the provided text. "
    "Rules: no preamble, no commentary, no 'Here is a summary' — just the summary itself. "
    "Keep it as short as possible while preserving all key facts. "
    "Use the same language as the input text."
)

ANSWER_BASE = (
    "You are a reply assistant. "
    "Given a message, write a clear and concise response to it. "
    "Rules: no preamble, no meta-commentary — just the reply itself. "
    "Match the language of the original message. "
    "Be direct and to the point."
)

class AITask(Enum):
    SUMMARIZE = SUMMARIZE_BASE
    ANSWER = ANSWER_BASE

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

# limits
MAX_MESSAGE_LENGTH = 4096

# Settings UI
CMD_SETTINGS = "settings"

TXT_SETTINGS_MAIN = "<b>Chat Settings</b>\n\nConfigure how the bot behaves in this chat."
TXT_SETTINGS_PRESETS = "<b>Choose AI Tone</b>\n\nSelect the personality preset for the AI responses:"
TXT_SETTINGS_CLOSED = "Settings menu closed."
TXT_ERR_ADMIN_ONLY = "Only administrators can change settings in groups."

BTN_AUTO_ON = "Mode: Auto 🟢"
BTN_AUTO_OFF = "Mode: Command ⚪"
BTN_TONE = "AI Tone: {tone}"
BTN_BACK = "Back"
BTN_CLOSE = "Close"

# Prompt presets
PROMPT_PRESETS = {
    "default": "",
    "friendly": "Act as a highly friendly, enthusiastic, and supportive assistant. Use emojis.",
    "official": "Act as a formal, strictly professional assistant. Be polite and use formal language.",
    "sarcastic": "Act as a sarcastic and slightly passive-aggressive assistant. Provide the correct output, but make subtle fun of the user in the process."
}