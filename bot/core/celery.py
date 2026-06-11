from celery import Celery
from bot.core.constants import BROKER

app = Celery('llm_call', broker=BROKER)