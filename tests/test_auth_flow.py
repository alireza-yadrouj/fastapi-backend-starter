from database import get_connection
from tests.database_test import get_test_connection


# tests register and login endpoint and token returns
def test_register_and_login_returns_token(auth_token):

    assert auth_token.status_code in [200, 201]

    access_token = auth_token.json()["access_token"]
    assert access_token is not None

#tests that wrong password in login endpoint returns stastus_code = 400
def test_login_with_wrong_password(client):
    # register user
    client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "correct_password",
            "role": "user"
        }
    )

    # login with wrong password
    response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "wrong_password"
        }
    )

    assert response.status_code == 400

#tests that non-existent username in login endpoint returns stastus_code = 400
def test_login_with_nonexistent_username(client):
    response = client.post(
        "/login",
        data={
            "username": "nonexistent_user",
            "password": "any_password"
        }
    )

    assert response.status_code == 400

#tests that duplicate username in register endpoint returns stastus_code = 400
def test_register_with_duplicate_username(client):
    client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "password123",
            "role": "user"
        }
    )

    response = client.post(
        "/register",
        json={
            "username": "duplicate_user",
            "password": "password123",
            "role": "user"
        }
    )

    assert response.status_code == 400






