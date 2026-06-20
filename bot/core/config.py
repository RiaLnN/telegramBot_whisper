from pydantic_settings import BaseSettings, SettingsConfigDict
from bot.core.groq_manager import GroqKeyManager
class BotSettings(BaseSettings):
    BOT_TOKEN: str = ''
    GROQ_KEYS: str = ''
    LLAMA_API_KEY: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = BotSettings()
groq_key_manager = GroqKeyManager(keys_string=settings.GROQ_KEYS, ban_duration=60)