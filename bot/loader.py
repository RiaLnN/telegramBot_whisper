from aiogram import Bot, Dispatcher
from bot.config import settings
from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties()
)

dp = Dispatcher()