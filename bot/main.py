import asyncio
from bot.loader import bot, dp
from bot.handlers import reply, voice
from bot.core.logger import setup_logger

async def start_bot():
    setup_logger()
    
    dp.include_router(router=voice.router)
    dp.include_router(router=reply.router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())