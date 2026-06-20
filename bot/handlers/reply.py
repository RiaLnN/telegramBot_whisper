from aiogram import Router, F
from aiogram.types import Message
from bot.core.constants import (
    SUMMARIZE_COMMANDS, ANSWER_COMMANDS, 
    MSG_PROCESSING_SUMMARY, MSG_PROCESSING_ANSWER,
    MSG_ERROR_SUMMARY, MSG_ERROR_ANSWER, AITask
)
from bot.service.settings import get_or_create_settings
from bot.tasks import process_text_task
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text, F.reply_to_message.text)
async def commands_handle(message: Message):
    if not message.text or not message.reply_to_message or not message.reply_to_message.text or not message.bot:
        return
    
    command = message.text.lower().strip()
    
    if command in SUMMARIZE_COMMANDS:
        task, proc_text, err_text = AITask.SUMMARIZE, MSG_PROCESSING_SUMMARY, MSG_ERROR_SUMMARY
    elif command in ANSWER_COMMANDS:
        task, proc_text, err_text = AITask.ANSWER, MSG_PROCESSING_ANSWER, MSG_ERROR_ANSWER
    else:
        return

    status_msg = await message.answer(proc_text)
    
    settings = await get_or_create_settings(message.chat.id)
    
    try:
        process_text_task.delay(
            raw_text=message.reply_to_message.text, 
            chat_id=message.chat.id, 
            message_id=status_msg.message_id, 
            task_name=task.name,  
            preset=settings.prompt_preset
        )
    except Exception as e:
        logger.error(f"Broker error: {e}")
        await status_msg.edit_text(err_text)