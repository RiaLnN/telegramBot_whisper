from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from bot.core.config import settings
from typing import AsyncGenerator

engine = create_async_engine(
    url=settings.database_url,
    echo=False,
    pool_size=5,
    max_overflow=10
)


async_session = async_sessionmaker(
    bind=engine, 
    class_=AsyncSession, 
    expire_on_commit=False
)

async def get_session() -> AsyncGenerator:
    async with async_session() as session:
        yield session