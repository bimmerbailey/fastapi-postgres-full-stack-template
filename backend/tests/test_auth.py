import pytest
from jose import jwt
from httpx import AsyncClient

from app import schemas
from app.config.config import settings

users_url = "/api/v1/users"
auth_url = "/api/v1/login"


@pytest.mark.anyio
async def test_create_user(client: AsyncClient):
    res = await client.post(
        users_url,
        json={"email": "hello123@gmail.com", "password": "password123"},
    )

    new_user = schemas.users.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


@pytest.mark.anyio
async def test_login_user(regular_user, client: AsyncClient):
    res = await client.post(
        auth_url,
        data={
            "username": regular_user.email,
            "password": regular_user.password,
        },
    )
    login_res = schemas.users.Token(**res.json())

    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.anyio
async def test_admin(client: AsyncClient, admin_user):
    res = await client.post(
        auth_url,
        data={
            "username": admin_user.email,
            "password": admin_user.password,
        },
    )
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert login_res.is_admin


@pytest.mark.anyio
async def test_regular_user(client: AsyncClient, regular_user):
    res = await client.post(
        auth_url,
        data={
            "username": regular_user.email,
            "password": regular_user.password,
        },
    )
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert not login_res.is_admin


@pytest.mark.parametrize(
    "email, password, status_code",
    [
        ("wrongemail@gmail.com", "password123", 401),
        ("michael@gmail.com", "wrongpassword", 401),
        ("wrongemail@gmail.com", "wrongpassword", 401),
        (None, "password123", 422),
        ("michael@gmail.com", None, 422),
    ],
)
@pytest.mark.anyio
async def test_incorrect_login(
    client: AsyncClient, email, password, status_code
):
    res = await client.post(
        auth_url, data={"username": email, "password": password}
    )

    assert res.status_code == status_code
