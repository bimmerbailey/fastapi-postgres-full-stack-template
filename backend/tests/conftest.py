import asyncio

from httpx import AsyncClient
import pytest
from asgi_lifespan import LifespanManager

from app import oauth
from app.main import app
from app.models.users import Users
from app.models.base import Base
from app.database.init_db import engine

# All test coroutines will be treated as marked.
pytestmark = pytest.mark.asyncio


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
async def client() -> AsyncClient:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async with LifespanManager(app):
        async with AsyncClient(
            app=app, base_url="http://localhost:3000"
        ) as client:
            yield client


@pytest.fixture
async def regular_user(client) -> Users:
    user_data = {"email": "user@gmail.com", "password": "password123"}
    res = await client.post("api/v1/users", json=user_data)

    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return Users(**new_user)


@pytest.fixture
async def admin_user(client) -> Users:
    user_data = {
        "email": "admin@gmail.com",
        "password": "password123",
        "is_admin": "true",
    }
    res = await client.post("api/v1/users", json=user_data)
    assert res.status_code == 201

    new_user = res.json()
    new_user["password"] = user_data["password"]
    return Users(**new_user)


@pytest.fixture
def token(test_user):
    return oauth.create_access_token({"user_id": test_user["id"]})


@pytest.fixture
async def authorized_client(client: AsyncClient, admin_user: Users):
    res = await client.post(
        "/api/v1/login",
        data={"username": admin_user.email, "password": admin_user.password},
    )

    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {res.json()['access_token']}",
    }

    yield client
