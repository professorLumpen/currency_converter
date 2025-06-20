from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


async_database_engine = create_async_engine(settings.ASYNC_DATABASE_URL)
async_database_session = async_sessionmaker(bind=async_database_engine, class_=AsyncSession)


class Base(DeclarativeBase):
    pass


async def get_async_session() -> AsyncGenerator:
    async with async_database_session() as session:
        yield session
