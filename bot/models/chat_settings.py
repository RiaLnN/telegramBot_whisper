from sqlalchemy import BigInteger, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column
from bot.models.base import Base

class ChatSettings(Base):
    __tablename__ = "chat_settings"

    chat_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    is_auto_mode: Mapped[bool] = mapped_column(Boolean, default=True)
    prompt_preset: Mapped[str] = mapped_column(String(50), default="default")