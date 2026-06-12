import asyncio
import os
import logging
from bot.core.celery import app
from bot.service.groq_api import get_voice_text
from bot.service.llama_api import get_ai_answer
from bot.core.constants import (
    ERROR_EMPTY_AUDIO, MAX_MESSAGE_LENGTH,
    ERROR_TELEGRAM_API, AITask, ERROR_EMPTY_AI_RESPONSE,
    ERROR_TEXT_RENDER, ERROR_UNEXPECTED
)
from bot.core.config import settings
from bot.core.exceptions import BotBaseException
from aiogram import Bot
from aiogram.exceptions import TelegramAPIError

@app.task
def process_voice_task(file_path: str, chat_id: int, message_id: int):
    bot = Bot(token=settings.BOT_TOKEN)

    async def run_logic():
        try:
            text = await get_voice_text(file_path=file_path)

            if not text or not text.strip():
                text = ERROR_EMPTY_AUDIO

            if len(text) > MAX_MESSAGE_LENGTH:
                text = text[: MAX_MESSAGE_LENGTH - 3] + "..."

            await bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=text
            )

        except BotBaseException as e:
            logging.warning(f"Business logic error in voice task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=str(e)
                )
            except Exception:
                pass

        except TelegramAPIError as e:
            logging.error(f"Telegram API Error in voice task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=ERROR_TELEGRAM_API
                )
            except Exception:
                pass

        except Exception as e:
            logging.exception(f"Unexpected error in voice task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=ERROR_UNEXPECTED
                )
            except Exception:
                pass

        finally:
            await bot.session.close()
            if os.path.exists(file_path):
                os.remove(file_path)

    asyncio.run(run_logic())


@app.task
def process_text_task(raw_text: str, chat_id: int, message_id: int, task_value: str):
    bot = Bot(token=settings.BOT_TOKEN)
    task = AITask(task_value)
    
    async def run_logic():
        try:
            text = await get_ai_answer(raw_text=raw_text, task=task)

            if not text or not text.strip():
                text = ERROR_EMPTY_AI_RESPONSE

            if len(text) > MAX_MESSAGE_LENGTH:
                text = text[: MAX_MESSAGE_LENGTH - 3] + "..."

            await bot.edit_message_text(
                chat_id=chat_id, message_id=message_id, text=text
            )

        except BotBaseException as e:
            logging.warning(f"Business logic error in text task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=str(e)
                )
            except Exception:
                pass

        except TelegramAPIError as e:
            logging.error(f"Telegram API Error in text task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=ERROR_TEXT_RENDER
                )
            except Exception:
                pass

        except Exception as e:
            logging.exception(f"Unexpected error in text task: {e}")
            try:
                await bot.edit_message_text(
                    chat_id=chat_id, message_id=message_id, text=ERROR_UNEXPECTED
                )
            except Exception:
                pass

        finally:
            await bot.session.close()

    asyncio.run(run_logic())