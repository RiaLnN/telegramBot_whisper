from aiogram import Router, F, Bot
from aiogram.types import Message
from bot.helpers import get_destination_path
from bot.tasks import process_voice_task

router = Router()

@router.message(F.voice)
async def voice_handle(message: Message, bot: Bot):
    file_id = message.voice.file_id if message.voice else 'N/A'

    status_msg = await message.answer("Transcribing voice message...")

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    if file_path:
        local_path = get_destination_path(file_id)
        await bot.download_file(file_path, local_path)
        
        process_voice_task.delay(
            file_path = local_path, 
            chat_id = message.chat.id, 
            message_id = status_msg.message_id)