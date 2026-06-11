from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseSettings):
    BOT_TOKEN: str = ''
    GROQ_API_KEY: str = ''
    LLAMA_API_KEY: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = BotSettings()
