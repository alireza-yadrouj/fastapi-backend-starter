from schemas.user import CurrentUser
from schemas.case import CaseCreate, CaseUpdate
from main import app, get_current_user


def _override_usre_a():
    return CurrentUser(
        username= "user_a",
        role= "user"
        )

def _override_usre_b():
    return CurrentUser(
        username= "user_b",
        role= "user"
        )

def _override_admin():
    return CurrentUser(
        username= "admin",
        role= "admin"
        )


#Create Case tests-------------------------------------

def test_user_can_create_case(client):

    case = CaseCreate(
        title = "case a",
        description= "case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case.model_dump() )

    assert post_response.status_code == 201

    data = post_response.json()
    assert data["id"] != None
    assert data["title"] == "case a"
    assert data["description"] == "case a desc"
    assert data["owner_username"] == "user_a"
    app.dependency_overrides.pop(get_current_user)

def test_admin_can_create_case(client):

    case = CaseCreate(
        title = "case admin",
        description= "case admin desc"
    )

    app.dependency_overrides[get_current_user] = _override_admin
    post_response = client.post("/cases", json=case.model_dump() )

    assert post_response.status_code == 201

    data = post_response.json()
    assert data["id"] != None
    assert data["title"] == "case admin"
    assert data["description"] == "case admin desc"
    assert data["owner_username"] == "admin"
    app.dependency_overrides.pop(get_current_user)

def test_NotAuthenticated_user_cannot_create_case(client):

    case = CaseCreate(
        title = "case test",
        description= "case test desc"
    )
    
    post_response = client.post("/cases", json=case.model_dump() )
    assert post_response.status_code == 401
#------------------------------------------------------



# get cases tests -------------------------------------

def test_user_can_get_own_cases(client):

    case = CaseCreate(
        title = "case a",
        description= "case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case.model_dump() )
    assert post_response.status_code == 201

    get_response = client.get("/cases")
    assert get_response.status_code == 200

    data = get_response.json()
    assert data["total"] == 1

    item = data["items"][0] 
    assert item["title"] == "case a"
    assert item["description"] == "case a desc"
    assert item["owner_username"] == "user_a"

    app.dependency_overrides.pop(get_current_user)

def test_admin_can_get_all_cases(client):

    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    case_b = CaseCreate(
        title = "case b",
        description= "case b desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_usre_b
    post_response = client.post("/cases", json=case_b.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_admin
    get_response = client.get("/cases")
    assert get_response.status_code == 200
    
    data = get_response.json()
    assert data["total"] == 2
    
    item_a = data["items"][0] 
    assert item_a["title"] == "case a"
    assert item_a["description"] == "case a desc"
    assert item_a["owner_username"] == "user_a"
    
    item_b = data["items"][1] 
    assert item_b["title"] == "case b"
    assert item_b["description"] == "case b desc"
    assert item_b["owner_username"] == "user_b"

    app.dependency_overrides.pop(get_current_user)

def test_user_cannot_get_other_user_cases(client):
    
    case = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_usre_b
    get_response = client.get("/cases")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["total"] == 0
    app.dependency_overrides.pop(get_current_user)

def test_NotAuthenticated_user_cannot_use_get_cases_endpoint(client):
    get_response = client.get("/cases" )
    assert get_response.status_code == 401
#------------------------------------------------------


#delete cases tests ------------------------------------
def test_user_can_delete_own_cases(client):

    case = CaseCreate(
        title = "case a",
        description= "case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case.model_dump() )
    assert post_response.status_code == 201
    

    delete_response = client.delete("/cases/1")
    assert delete_response.status_code == 204

    app.dependency_overrides.pop(get_current_user)

def test_admin_can_delete_all_cases(client):
    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    case_admin = CaseCreate(
        title = "case admin",
        description= "case admin desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_admin
    post_response = client.post("/cases", json=case_admin.model_dump() )
    assert post_response.status_code == 201
    
    delete_a_response = client.delete("/cases/1")
    assert delete_a_response.status_code == 204
    delete_admin_response = client.delete("/cases/2")
    assert delete_admin_response.status_code == 204

def test_user_cannot_delete_other_user_cases(client):
    
    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_usre_b
    delete_response = client.delete("/cases/1")
    assert delete_response.status_code == 403
    app.dependency_overrides.pop(get_current_user)

def test_NotAuthenticated_user_cannot_use_delete_cases_endpoint(client):
    delete_response = client.delete("/cases/1")
    assert delete_response.status_code == 401
#-------------------------------------------------------


#update cases tests-------------------------------------
def tests_user_can_update_own_cases(client):

    case = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    updated_case = CaseUpdate(
        title = "updated case a",
        description = "updates case a desc"
    )
    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case.model_dump() )
    assert post_response.status_code == 201

    update_response = client.patch("/cases/1", json=updated_case.model_dump())
    assert update_response.status_code == 200
    
    data = update_response.json()
    assert data["id"] == 1
    assert data["title"] == "updated case a"
    assert data["description"] == "updates case a desc"
    assert data["owner_username"] == "user_a"

    app.dependency_overrides.pop(get_current_user)

def test_admin_can_update_all_cases(client):

    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    case_admin = CaseCreate(
        title = "case admin",
        description= "case admin desc"
    )
    updated_case_a = CaseUpdate(
        title = "updated case a",
        description = "updates case a desc"
    )
    updated_case_admin = CaseUpdate(
        title = "updated case admin",
        description = "updates case admin desc"
    )
    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_admin
    post_response = client.post("/cases", json=case_admin.model_dump() )
    assert post_response.status_code == 201

    update_response_a = client.patch("/cases/1", json=updated_case_a.model_dump())
    assert update_response_a.status_code == 200
    data = update_response_a.json()
    assert data["id"] == 1
    assert data["title"] == "updated case a"
    assert data["description"] == "updates case a desc"
    assert data["owner_username"] == "user_a"

    update_response_admin = client.patch("/cases/2", json=updated_case_admin.model_dump())
    assert update_response_admin.status_code == 200
    data = update_response_admin.json()
    assert data["id"] == 2
    assert data["title"] == "updated case admin"
    assert data["description"] == "updates case admin desc"
    assert data["owner_username"] == "admin"

    app.dependency_overrides.pop(get_current_user)

def test_user_cannot_update_cases_other_user(client):
    
    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    updated_case_a = CaseUpdate(
        title = "updated case a",
        description = "updates case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    app.dependency_overrides[get_current_user] = _override_usre_b
    update_response = client.patch("/cases/1", json=updated_case_a.model_dump())
    assert update_response.status_code == 403
    app.dependency_overrides.pop(get_current_user)

def test_NotAuthenticated_user_cannot_use_update_cases_endpoint(client):
    
    case_a = CaseCreate(
        title = "case a",
        description= "case a desc"
    )
    updated_case_a = CaseUpdate(
        title = "updated case a",
        description = "updates case a desc"
    )

    app.dependency_overrides[get_current_user] = _override_usre_a
    post_response = client.post("/cases", json=case_a.model_dump() )
    assert post_response.status_code == 201
    app.dependency_overrides.pop(get_current_user)

    update_response = client.patch("/cases/1", json =updated_case_a.model_dump())
    assert update_response.status_code == 401

