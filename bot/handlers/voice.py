from aiogram import Router, F, Bot
from aiogram.types import Message
from bot.helpers import get_destination_path
from bot.tasks import process_voice_task
from bot.core.constants import MSG_PROCESSING_VOICE, MSG_ERROR_VOICE, TRANSCRIBE_COMMANDS
from bot.service.settings import get_or_create_settings
import logging

logger = logging.getLogger(__name__)
router = Router()


async def _run_transcription(media_obj, message: Message, bot: Bot):
    file_id = media_obj.file_id
    status_msg = await message.answer(MSG_PROCESSING_VOICE)

    try:
        process_voice_task.delay(
            file_id=file_id,
            chat_id=message.chat.id,
            message_id=status_msg.message_id
        )
    except Exception as e:
        logger.error(f"Failed to queue voice task: {e}")
        await status_msg.edit_text(MSG_ERROR_VOICE)


@router.message(F.voice | F.video_note)
async def voice_handle(message: Message, bot: Bot):
    settings = await get_or_create_settings(message.chat.id)

    if not settings.is_auto_mode:
        return

    media_obj = message.voice or message.video_note
    if not media_obj:
        return

    await _run_transcription(media_obj, message, bot)


@router.message(F.text, F.reply_to_message.voice | F.reply_to_message.video_note)
async def voice_command_handle(message: Message, bot: Bot):
    if not message.text or not message.reply_to_message:
        return

    command = message.text.lower().strip()
    if command not in TRANSCRIBE_COMMANDS:
        return

    settings = await get_or_create_settings(message.chat.id)
    if settings.is_auto_mode:
        return

    media_obj = message.reply_to_message.voice or message.reply_to_message.video_note
    if not media_obj:
        return

    await _run_transcription(media_obj, message, bot)