from typing import AsyncGenerator

import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.core.config import settings
from app.db.database import Base, get_async_session
from main import app


@pytest.fixture
async def test_session():
    test_engine = create_async_engine(settings.TEST_DATABASE_URL)
    test_session_maker = async_sessionmaker(test_engine, class_=AsyncSession)

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with test_session_maker() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture
async def test_app(test_session):
    async def get_test_session() -> AsyncGenerator:
        yield test_session

    app.dependency_overrides[get_async_session] = get_test_session
    yield app


@pytest.fixture
async def async_client(test_app):
    transport = ASGITransport(test_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_token(async_client):
    register_data = {"username": "string", "password": "stringstri"}
    await async_client.post("/auth/register/", json=register_data)
    response = await async_client.post("/auth/login/", json=register_data)
    token = response.json()["token"]
    return token
