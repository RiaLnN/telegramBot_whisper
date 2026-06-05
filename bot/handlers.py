from aiogram import Router, F, Bot
from aiogram.types import Message
from helpers import get_destination_path
from service import get_voice_text
from llm_service import enrich_text_with_emotions
import os


router = Router()

@router.message(F.voice)
async def voice_handle(message: Message, bot: Bot):
    file_id = message.voice.file_id if message.voice else 'N/A'

    status_message = await message.answer("Расшифровываю голосовое сообщение...")

    file_info = await bot.get_file(file_id)
    file_path = file_info.file_path

    if file_path:
        local_path = get_destination_path(file_id)
        await bot.download_file(file_path, local_path)
        
        recognized_text, success = await get_voice_text(local_path)
        
        if success:
            await status_message.edit_text("Анализирую эмоции и причесываю текст...")
            final_text = await enrich_text_with_emotions(recognized_text)

            await status_message.edit_text(f"**Результат:**\n\n{final_text}", parse_mode="Markdown")
        else:
            await status_message.edit_text("Не удалось распознать речь.")
            
        if os.path.exists(local_path):
            os.remove(local_path)