import pytest
from fastapi.testclient import TestClient
from main import app  
from tests.test_setup import reset_cases_table

# ریست دیتابیس قبل از اجرای تست‌ها
reset_cases_table()


client = TestClient(app)

client.post("/register", json={"username": "user1", "password": "password1"})
client.post("/register", json={"username": "user2", "password": "password2"})


def test_example():
    response = client.get("/cases")
    assert response.status_code == 401  

def get_token(username, password):
    response = client.post(
        "/login",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]

user1_token = get_token("user1", "password1")
user2_token = get_token("user2", "password2")

headers_user1 = {"Authorization": f"Bearer {user1_token}"}
headers_user2 = {"Authorization": f"Bearer {user2_token}"}

def test_create_cases():
    # user1 یک کیس می‌سازد
    response = client.post(
        "/cases",
        json={"title": "User1 Case", "description": "Desc1"},
        headers=headers_user1
    )
    assert response.status_code == 201

    # user2 یک کیس می‌سازد
    response = client.post(
        "/cases",
        json={"title": "User2 Case", "description": "Desc2"},
        headers=headers_user2
    )
    assert response.status_code == 201

def test_get_cases():
    # user1 فقط کیس خودش را می‌بیند
    response = client.get("/cases", headers=headers_user1)
    assert response.status_code == 200
    cases = response.json()
    assert all(c["owner_username"] == "user1" for c in cases)

    # user2 فقط کیس خودش را می‌بیند
    response = client.get("/cases", headers=headers_user2)
    assert response.status_code == 200
    cases = response.json()
    assert all(c["owner_username"] == "user2" for c in cases)

def test_patch_case():
    # user1 کیس خودش را آپدیت می‌کند
    response = client.patch(
        "/cases/1", 
        json={"title": "User1 Case Updated"},
        headers=headers_user1
    )
    assert response.status_code == 204  # موفقیت بدون محتوا

    # user2 تلاش می‌کند کیس user1 را آپدیت کند
    response = client.patch(
        "/cases/1",
        json={"title": "Hacked by User2"},
        headers=headers_user2
    )
    assert response.status_code == 403  # Forbidden

def test_delete_case():
    # user1 کیس خودش را حذف می‌کند
    response = client.delete("/cases/1", headers=headers_user1)
    assert response.status_code == 204

    # user2 تلاش می‌کند کیس user2 را حذف کند (موفق)
    response = client.delete("/cases/2", headers=headers_user2)
    assert response.status_code == 204

    # user2 تلاش می‌کند کیس غیر موجود را حذف کند
    response = client.delete("/cases/1", headers=headers_user2)
    assert response.status_code == 404  # Case already deleted
