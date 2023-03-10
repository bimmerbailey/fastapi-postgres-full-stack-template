import pytest
from jose import jwt
from fastapi.testclient import TestClient

from app import schemas
from app.config.config import settings

users_url = "/api/v1/users"
auth_url = "/api/v1/login"


def test_create_user(client):
    res = client.post(
        users_url, json={"email": "hello123@gmail.com", "password": "password123"})

    new_user = schemas.users.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201


def test_login_user(regular_user, client):
    res = client.post(
        auth_url, data={"username": regular_user['email'], "password": regular_user['password']})
    login_res = schemas.users.Token(**res.json())
    payload = jwt.decode(login_res.access_token,
                         settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == regular_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


def test_admin(client: TestClient, admin_user):
    res = client.post(
        auth_url, data={"username": admin_user['email'], "password": admin_user['password']})
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert login_res.is_admin


def test_regular_user(client: TestClient, regular_user):
    res = client.post(
        auth_url, data={"username": regular_user['email'], "password": regular_user['password']})
    login_res = schemas.users.Token(**res.json())
    assert res.status_code == 200
    assert not login_res.is_admin


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 401),
    ('michael@gmail.com', 'wrongpassword', 401),
    ('wrongemail@gmail.com', 'wrongpassword', 401),
    (None, 'password123', 422),
    ('michael@gmail.com', None, 422)
])
def test_incorrect_login(client, email, password, status_code):
    res = client.post(
        auth_url, data={"username": email, "password": password})

    assert res.status_code == status_code
