import pytest
import os
import database
from fastapi.testclient import TestClient
from tests.database_test import get_test_connection, init_test_db
from main import app as fastapi_app
from schemas.user import CurrentUser
from core.security import get_current_user


database.get_connection = get_test_connection

#returns app in main file
@pytest.fixture
def app():
    return fastapi_app

# removes database then creates empty database
@pytest.fixture(autouse=True)
def setup_test_db(monkeypatch):
    if os.path.exists("test_database.db"):
        os.remove("test_database.db")

    init_test_db()
    monkeypatch.setattr(database, "DB_name", "test_database.db")

    yield

    if os.path.exists("test_database.db"):
        os.remove("test_database.db")

#create a client test
@pytest.fixture
def client (app):
    return TestClient(app)

# registers and then logs in then returns token
@pytest.fixture
def auth_token(client: TestClient) -> str:

    client.post(
        "/register",
        json={
            "username": "testuser",
            "password": "testpassword",
            "role": "user"
        }
    )

    login_response = client.post(
        "/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )

    return login_response

#mocks normal user_a
@pytest.fixture
def user_a(app):
    def override():
        return CurrentUser(username="user_a", role="user")
    
    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()

#mocks normal user_b
@pytest.fixture
def user_b(app):
    def override():
        return CurrentUser(username="user_b", role="user")

    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()

#mocks admin
@pytest.fixture
def admin_user(app):
    def override():
        return CurrentUser(username="admin", role="admin")
    
    app.dependency_overrides[get_current_user] = override
    yield
    app.dependency_overrides.clear()




