from aiogram import Router, F
from aiogram.types import Message
from bot.core.constants import (
    SUMMARIZE_COMMANDS, ANSWER_COMMANDS, 
    MSG_PROCESSING_SUMMARY, MSG_PROCESSING_ANSWER,
    MSG_ERROR_SUMMARY, MSG_ERROR_ANSWER,
)
from bot.core.constants import AITask
from bot.tasks import process_text_task

router = Router()

@router.message(F.text, F.reply_to_message)
async def commands_handle(message: Message):
    if not message.text or not message.reply_to_message or not message.reply_to_message.text or not message.bot or not message.reply_to_message.from_user:
        return
    
    command = message.text.lower().strip()
    
    bot_user = await message.bot.me()
    if message.reply_to_message.from_user.id != bot_user.id:
        return

    if command in SUMMARIZE_COMMANDS:
        task, proc_text, err_text = AITask.SUMMARIZE, MSG_PROCESSING_SUMMARY, MSG_ERROR_SUMMARY
    elif command in ANSWER_COMMANDS:
        task, proc_text, err_text = AITask.ANSWER, MSG_PROCESSING_ANSWER, MSG_ERROR_ANSWER
    else:
        return

    status_msg = await message.answer(proc_text)
    
    try:
        process_text_task.delay(
            raw_text = message.reply_to_message.text, 
            chat_id = message.chat.id, 
            message_id = status_msg.message_id, 
            task_value = task.value
        )
    except Exception as e:
        await status_msg.edit_text(err_text)
