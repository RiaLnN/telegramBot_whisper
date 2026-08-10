from typing import Union
from aiogram.filters import BaseFilter
from aiogram.types import Message, Voice, VideoNote, Audio, Video, Document

MediaUnion = Union[Voice, VideoNote, Audio, Video, Document]

ALLOWED_EXTENSIONS = (
    '.mp3', '.mp4', '.ogg', '.wav', '.m4a', 
    '.aac', '.flac', '.mov', '.avi', '.mkv', '.webm'
)

class HasAudioOrVideoFilter(BaseFilter):
    def __init__(self, check_reply: bool = False):
        self.check_reply = check_reply

    async def __call__(self, message: Message) -> dict[str, MediaUnion] | bool:
        target_msg = message.reply_to_message if self.check_reply else message
        
        if not target_msg:
            return False

        media = target_msg.voice or target_msg.video_note or target_msg.audio or target_msg.video
        if media:
            return {"media_obj": media}

        doc = target_msg.document
        if doc:
            mime = (doc.mime_type or "").lower()
            if mime.startswith("audio/") or mime.startswith("video/"):
                return {"media_obj": doc}

            file_name = (doc.file_name or "").lower()
            if file_name.endswith(ALLOWED_EXTENSIONS):
                return {"media_obj": doc}

        return False