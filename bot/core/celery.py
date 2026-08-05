from celery import Celery
from bot.core.config import settings

app = Celery('llm_call', broker=settings.redis_dsn)