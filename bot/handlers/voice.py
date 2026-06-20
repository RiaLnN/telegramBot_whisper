from aiogram import Router, F, Bot
from aiogram.types import Message
from bot.helpers import get_destination_path
from bot.tasks import process_voice_task
from bot.core.constants import MSG_PROCESSING_VOICE, MSG_ERROR_VOICE
import logging

router = Router()

@router.message(F.voice | F.video_note)
async def voice_handle(message: Message, bot: Bot):
    media_obj = message.voice or message.audio or message.video_note

    if not media_obj:
        return

    file_id = media_obj.file_id
    status_msg = await message.answer(MSG_PROCESSING_VOICE)

    try:
        file_info = await bot.get_file(file_id)
        file_path = file_info.file_path

        if file_path:
            local_path = get_destination_path(file_id)
            await bot.download_file(file_path, local_path)
            
            process_voice_task.delay(
                file_path=local_path, 
                chat_id=message.chat.id, 
                message_id=status_msg.message_id
            )
        else:
            await status_msg.edit_text("Failed to get audio file path.")
            
    except Exception as e:
        logging.error(f"Voice handler error: {e}")
        await status_msg.edit_text(MSG_ERROR_VOICE)