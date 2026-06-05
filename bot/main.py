import asyncio
from loader import bot, dp
from handlers import router
import logging

async def start_bot():
    logging.basicConfig(level=logging.INFO)
    dp.include_router(router=router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())