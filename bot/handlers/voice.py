from aiogram import Router, F, Bot
from aiogram.types import Message
from bot.helpers import get_destination_path
from bot.service.groq_api import get_voice_text
import os

router = Router()

@router.message(F.voice)
async def voice_handle(message: Message, bot: Bot):
    file_id = message.voice.file_id if message.voice else 'N/A'

    status_message = await message.answer("Transcribing voice message...")

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    if file_path:
        local_path = get_destination_path(file_id)
        await bot.download_file(file_path, local_path)
        
        recognized_text = await get_voice_text(local_path)
        await status_message.edit_text(recognized_text)
            
        if os.path.exists(local_path):
            os.remove(local_path)