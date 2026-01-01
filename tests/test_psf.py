from schemas.case import CaseCreate
from main import app
from core.security import CurrentUser , get_current_user

def _override_usre_a():
    return CurrentUser(
        username= "user_a",
        role= "user"
        )

case1 = CaseCreate(
    title = "alice",
    description= "device"
)
case2 = CaseCreate(
    title="branch",
    description="equal"
)
case3 = CaseCreate(
    title= "craft",
    description="france"
)

#sorting test-------------------------------------------
def test_sorting_by_title_asc_and_desc(client):

    app.dependency_overrides[get_current_user] = _override_usre_a
    response1 = client.post("/cases", json=case2.model_dump())
    assert response1.status_code == 201
    response2 = client.post("/cases", json=case3.model_dump())
    assert response2.status_code == 201
    response3 = client.post("/cases", json=case1.model_dump())
    assert response3.status_code == 201

    request1 = client.get("/cases?sort_by=title&sort_order=asc")
    assert request1.status_code == 200
    data = request1.json()["items"]
    titles = [item["title"] for item in data]
    assert titles == sorted(titles)

    request2 = client.get("/cases?sort_by=title&sort_order=desc")
    assert request2.status_code == 200
    data = request2.json()["items"]
    titles = [item["title"] for item in data]
    assert titles == sorted(titles, reverse=True)

    app.dependency_overrides.pop(get_current_user)

def test_sorting_by_description_asc_and_desc(client):
    app.dependency_overrides[get_current_user] = _override_usre_a
    response1 = client.post("/cases", json=case2.model_dump())
    assert response1.status_code == 201
    response2 = client.post("/cases", json=case3.model_dump())
    assert response2.status_code == 201
    response3 = client.post("/cases", json=case1.model_dump())
    assert response3.status_code == 201

    request1 = client.get("/cases?sort_by=description&sort_order=asc")
    assert request1.status_code == 200
    data = request1.json()["items"]
    titles = [item["description"] for item in data]
    assert titles == sorted(titles)

    request2 = client.get("/cases?sort_by=description&sort_order=desc")
    assert request2.status_code == 200
    data = request2.json()["items"]
    titles = [item["description"] for item in data]
    assert titles == sorted(titles, reverse=True)

    app.dependency_overrides.pop(get_current_user)
#-------------------------------------------------------


#filtering test-----------------------------------------
def test_filtering_by_title(client):

    app.dependency_overrides[get_current_user] = _override_usre_a
    response1 = client.post("/cases", json=case1.model_dump())
    assert response1.status_code == 201
    response2 = client.post("/cases", json=case2.model_dump())
    assert response2.status_code == 201
    response3 = client.post("/cases", json=case3.model_dump())
    assert response3.status_code == 201

    request1 = client.get("/cases?title=ra")
    assert request1.status_code == 200
    data = request1.json()["items"]
    titles = [item["title"] for item in data]
    assert titles == ["branch", "craft"]

    app.dependency_overrides.pop(get_current_user)

def test_filtering_by_description(client):

    app.dependency_overrides[get_current_user] = _override_usre_a
    response1 = client.post("/cases", json=case1.model_dump())
    assert response1.status_code == 201
    response2 = client.post("/cases", json=case2.model_dump())
    assert response2.status_code == 201
    response3 = client.post("/cases", json=case3.model_dump())
    assert response3.status_code == 201

    request1 = client.get("/cases?description=ce")
    assert request1.status_code == 200
    data = request1.json()["items"]
    titles = [item["description"] for item in data]
    assert titles == ["device", "france"]
    
    app.dependency_overrides.pop(get_current_user)
#-------------------------------------------------------


#pagination test----------------------------------------
def test_pagination(client):

    app.dependency_overrides[get_current_user] = _override_usre_a
    response1 = client.post("/cases", json=case1.model_dump())
    assert response1.status_code == 201
    response2 = client.post("/cases", json=case2.model_dump())
    assert response2.status_code == 201
    response3 = client.post("/cases", json=case3.model_dump())
    assert response3.status_code == 201

    request1 = client.get("/cases?page=1&page_size=2")
    assert request1.status_code == 200
    data = request1.json()["items"]
    assert len(data) == 2

    request2 = client.get("/cases?page=2&page_size=2")
    assert request2.status_code == 200
    data = request2.json()["items"]
    assert len(data) == 1

    request3 = client.get("/cases?page=3&page_size=2")
    assert request3.status_code == 200
    data = request3.json()["items"]
    assert len(data) == 0

    app.dependency_overrides.pop(get_current_user)
#-------------------------------------------------------

