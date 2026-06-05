from pydantic_settings import BaseSettings, SettingsConfigDict

class BotSettings(BaseSettings):
    BOT_TOKEN: str = ''
    WHISPER_URL: str = ''
    HF_TOKEN: str = ''
    API_URL: str = ''

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8'
    )

settings = BotSettings()
