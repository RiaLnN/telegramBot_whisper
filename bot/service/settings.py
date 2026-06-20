from sqlalchemy import select
from bot.core.database import async_session
from bot.models.chat_settings import ChatSettings


async def _fetch_or_create(session, chat_id: int) -> ChatSettings:
    result = await session.execute(
        select(ChatSettings).where(ChatSettings.chat_id == chat_id)
    )
    settings = result.scalar_one_or_none()

    if not settings:
        settings = ChatSettings(
            chat_id=chat_id,
            is_auto_mode=True,
            prompt_preset="default"
        )
        session.add(settings)
        await session.commit()
        await session.refresh(settings)

    return settings


async def get_or_create_settings(chat_id: int) -> ChatSettings:
    async with async_session() as session:
        return await _fetch_or_create(session, chat_id)


async def toggle_auto_mode(chat_id: int) -> bool:
    async with async_session() as session:
        settings = await _fetch_or_create(session, chat_id)
        settings.is_auto_mode = not settings.is_auto_mode
        await session.commit()
        return settings.is_auto_mode


async def update_preset(chat_id: int, new_preset: str) -> None:
    async with async_session() as session:
        settings = await _fetch_or_create(session, chat_id)
        settings.prompt_preset = new_preset
        await session.commit()