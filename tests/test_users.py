import asyncio

import pytest


@pytest.mark.asyncio
async def test_register_and_login(async_client):
    register_data = {"username": "string", "password": "stringstri"}

    response = await async_client.post("/auth/register/", json=register_data)
    data = response.json()
    assert response.status_code == 200
    assert data["username"] == "string"
    assert data["id"] == 1

    response = await async_client.post("/auth/login/", json=register_data)
    data = response.json()
    assert response.status_code == 200
    assert "token" in data
    assert data["type"] == "bearer"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, message",
    [
        ("nick", "password1234", "String should have at least 5 characters"),
        ("nick" * 10, "password1234", "String should have at most 30 characters"),
        ("nickname", "password", "String should have at least 10 characters"),
        (None, "password1234", "Field required"),
    ],
)
async def test_wrong_register(username, password, message, async_client):
    register_data = {"password": password}
    if username is not None:
        register_data["username"] = username

    response = await async_client.post("/auth/register/", json=register_data)
    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == message


@pytest.mark.asyncio
async def test_register_twice(async_client):
    register_data = {"username": "string", "password": "stringstri"}

    response = await async_client.post("/auth/register/", json=register_data)
    assert response.status_code == 200

    await asyncio.sleep(1)

    response = await async_client.post("/auth/register/", json=register_data)
    assert response.status_code == 403
    assert response.json() == {"detail": "Object already exists"}


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username, password, status_code, message",
    [
        ("username", "stringstri1", 401, "Incorrect username or password"),
        ("username1", "stringstri", 404, "Object not found"),
        (None, "stringstri", 422, "Field required"),
    ],
)
async def test_wrong_login(username, password, status_code, message, async_client):
    register_data = {"username": "username", "password": "stringstri"}
    response = await async_client.post("/auth/register/", json=register_data)
    assert response.status_code == 200

    login_data = {"password": password}
    if username is not None:
        login_data["username"] = username

    response = await async_client.post("/auth/login/", json=login_data)
    detail = response.json()["detail"]
    if isinstance(detail, list):
        detail = detail[0]["msg"]
    assert response.status_code == status_code
    assert detail == message
