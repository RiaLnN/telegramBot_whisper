from pydantic_settings import BaseSettings, SettingsConfigDict
class BotSettings(BaseSettings):
    BOT_TOKEN: str = ''
    GROQ_KEYS: str = ''
    LLAMA_API_KEY: str = ''
    
    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_USER: str = 'bot_user'
    DB_PASS: str = 'bot_password'
    DB_NAME: str = 'bot_db'

    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        extra='ignore'
    )

    @property
    def database_url(self) -> str:
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = BotSettings()
