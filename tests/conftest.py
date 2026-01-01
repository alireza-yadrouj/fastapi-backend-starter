import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app as fastapi_app
from database import get_db
from database_test import get_test_session, init_test_db, drop_test_db

@pytest.fixture
def client():
    return TestClient(fastapi_app)

@pytest.fixture(autouse=True)
def override_get_db():
    def _override():
        db_gen = get_test_session()
        db = next(db_gen)
        try:
            yield db
        finally:
            try:
                next(db_gen)
            except StopIteration:
                pass

    fastapi_app.dependency_overrides[get_db] = _override
    yield
    fastapi_app.dependency_overrides.pop(get_db, None)


@pytest.fixture(autouse=True)
def setup_test_db():
    drop_test_db()
    init_test_db()
    yield
    drop_test_db()


