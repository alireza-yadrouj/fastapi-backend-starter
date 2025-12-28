from schemas.user import CurrentUser
from core.security import get_current_user
from main import app

def test_user_can_create_case(client, user_a, setup_test_db):
    response = client.post(
        "/cases",
        json={
            "title": "Test Case",
            "description": "Test Description"
        }
    )

    assert response.status_code == 201

def test_admin_can_create_case(client, admin_user, setup_test_db):
    response = client.post(
        "/cases",
        json={
            "title": "Admin Case",
            "description": "Admin Description"
        }
    )

    assert response.status_code == 201

def test_unauthenticated_user_cannot_create_case(client, setup_test_db):
    response = client.post(
        "/cases",
        json={
            "title": "Unauthorized Case",
            "description": "Should Fail"
        }
    )

    assert response.status_code == 401

def test_user_can_get_own_cases(client, user_a, setup_test_db):
    
    payload = {
        "title": "User Case",
        "description": "Case created by user_a"
    }
    post_response = client.post("/cases", json=payload)
    assert post_response.status_code == 201

    get_response = client.get("/cases")
    assert get_response.status_code == 200

    data = get_response.json()
    
    assert "items" in data  

    returned_case = data["items"][0]
    assert returned_case["title"] == payload["title"]
    assert returned_case["description"] == payload["description"]

def test_admin_can_get_all_cases_with_different_owners(client, setup_test_db):

    payload_a = {
        "title": "User A Case",
        "description": "Created by user_a"
    }
    payload_b = {
        "title": "User B Case",
        "description": "Created by user_b"
    }

    def override_user_a():
        return CurrentUser(username="user_a", role="user")

    app.dependency_overrides[get_current_user] = override_user_a
    post_response_a = client.post("/cases", json=payload_a)
    assert post_response_a.status_code == 201
    app.dependency_overrides.clear()  

    def override_user_b():
        return CurrentUser(username="user_b", role="user")

    app.dependency_overrides[get_current_user] = override_user_b
    post_response_b = client.post("/cases", json=payload_b)
    assert post_response_b.status_code == 201
    app.dependency_overrides.clear()  

    def override_admin():
        return CurrentUser(username="admin", role="admin")

    app.dependency_overrides[get_current_user] = override_admin
    get_response = client.get("/cases")
    assert get_response.status_code == 200

    data = get_response.json()
    assert "items" in data

    returned_titles = [case["title"] for case in data["items"]]
    assert payload_a["title"] in returned_titles
    assert payload_b["title"] in returned_titles

    app.dependency_overrides.clear() 

def test_user_b_cannot_see_user_a_case(client, setup_test_db):
    payload = {
        "title": "User A Case",
        "description": "Created by user_a"
    }

    def override_user_a():
        return CurrentUser(username="user_a", role="user")

    app.dependency_overrides[get_current_user] = override_user_a
    post_response = client.post("/cases", json=payload)
    assert post_response.status_code == 201
    app.dependency_overrides.clear()

    def override_user_b():
        return CurrentUser(username="user_b", role="user")

    app.dependency_overrides[get_current_user] = override_user_b
    get_response = client.get("/cases")
    data = get_response.json()

    assert get_response.status_code == 200
    assert len(data["items"]) == 0

    app.dependency_overrides.clear()

def test_client_without_token_cannot_access_cases(client, setup_test_db):
    get_response = client.get("/cases")

    assert get_response.status_code == 401

def test_admin_can_update_and_delete_any_case(client, setup_test_db):
   
    payload_a = {"title": "Case A", "description": "Created by user_a"}
    payload_b = {"title": "Case B", "description": "Created by user_b"}

   
    def override_user_a():
        return CurrentUser(username="user_a", role="user")

    app.dependency_overrides[get_current_user] = override_user_a

    post_a = client.post("/cases", json=payload_a)
    assert post_a.status_code == 201
    assert post_a.json() == {"message": "case created"}

   
    def override_user_b():
        return CurrentUser(username="user_b", role="user")

    app.dependency_overrides[get_current_user] = override_user_b

    post_b = client.post("/cases", json=payload_b)
    assert post_b.status_code == 201
    assert post_b.json() == {"message": "case created"}

    
    def override_admin():
        return CurrentUser(username="admin", role="admin")

    app.dependency_overrides[get_current_user] = override_admin

    get_all = client.get("/cases")
    assert get_all.status_code == 200

    items = get_all.json()["items"]

    case_a = next(case for case in items if case["owner_username"] == "user_a")
    case_b = next(case for case in items if case["owner_username"] == "user_b")

    
    updated_payload = {
        "title": "Updated by Admin",
        "description": "Admin updated"
    }

    patch_a = client.patch(f"/cases/{case_a['id']}", json=updated_payload)
    patch_b = client.patch(f"/cases/{case_b['id']}", json=updated_payload)

    assert patch_a.status_code == 204
    assert patch_b.status_code == 204

   
    get_after_update = client.get("/cases")
    assert get_after_update.status_code == 200

    updated_items = get_after_update.json()["items"]

    updated_case_a = next(case for case in updated_items if case["id"] == case_a["id"])
    updated_case_b = next(case for case in updated_items if case["id"] == case_b["id"])

    assert updated_case_a["title"] == updated_payload["title"]
    assert updated_case_b["title"] == updated_payload["title"]

   
    delete_a = client.delete(f"/cases/{case_a['id']}")
    delete_b = client.delete(f"/cases/{case_b['id']}")

    assert delete_a.status_code == 204
    assert delete_b.status_code == 204

   
    final_get = client.get("/cases")
    assert final_get.status_code == 200
    assert final_get.json()["items"] == []

   
    app.dependency_overrides.clear()

def test_user_cannot_update_or_delete_other_users_case(client):
    payload = {
        "title": "User A Case",
        "description": "Created by user_a"
    }

    def override_user_a():
        return CurrentUser(username="user_a", role="user")

    app.dependency_overrides[get_current_user] = override_user_a
    post_response = client.post("/cases", json=payload)
    assert post_response.status_code == 201

    def override_admin():
        return CurrentUser(username="admin", role="admin")

    app.dependency_overrides[get_current_user] = override_admin
    get_response = client.get("/cases")
    case_id = get_response.json()["items"][0]["id"]

    def override_user_b():
        return CurrentUser(username="user_b", role="user")

    app.dependency_overrides[get_current_user] = override_user_b
    patch_response = client.patch(
        f"/cases/{case_id}",
        json={"title": "Hacked title"}
    )
    assert patch_response.status_code in (403, 404)

    delete_response = client.delete(f"/cases/{case_id}")
    assert delete_response.status_code in (403, 404)

    app.dependency_overrides.clear()

def test_unauthenticated_user_cannot_update_or_delete_case(client):
    payload = {
        "title": "Admin Case",
        "description": "Created by admin"
    }

    def override_admin():
        return CurrentUser(username="admin", role="admin")

    app.dependency_overrides[get_current_user] = override_admin
    post_response = client.post("/cases", json=payload)
    assert post_response.status_code == 201

    get_response = client.get("/cases")
    case_id = get_response.json()["items"][0]["id"]

    app.dependency_overrides.clear()

    patch_response = client.patch(
        f"/cases/{case_id}",
        json={"title": "Unauthorized update"}
    )
    assert patch_response.status_code == 401

    delete_response = client.delete(f"/cases/{case_id}")
    assert delete_response.status_code == 401




