

# pagination tests.................
def test_user_can_paginate_own_cases(client, user_a):

    for i in range(6):
        response = client.post(
            "/cases",
            json={
                "title": f"case {i}",
                "description": "test pagination"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?page=1&page_size=5")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] == 6
    assert data["page"] == 1
    assert data["page_size"] == 5
    assert len(data["items"]) == 5

def test_user_can_get_second_page_of_cases(client, user_a):
    for i in range(6):
        response = client.post(
            "/cases",
            json={
                "title": f"case {i}",
                "description": "pagination test"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?page=2&page_size=5")

    assert response.status_code == 200
    data = response.json()

    assert data["page"] == 2
    assert data["page_size"] == 5
    assert data["total"] == 6
    assert len(data["items"]) == 1

def test_pagination_page_out_of_range_returns_empty_items(client, user_a):
    # Arrange: create 6 cases
    for i in range(6):
        response = client.post(
            "/cases",
            json={
                "title": f"case {i}",
                "description": "pagination test"
            }
        )
        assert response.status_code == 201

    # Act: request a page out of range
    response = client.get("/cases?page=10&page_size=5")

    # Assert
    assert response.status_code == 200
    data = response.json()

    assert data["page"] == 10
    assert data["page_size"] == 5
    assert data["total"] == 6
    assert data["items"] == []

def test_pagination_invalid_page_returns_422(client, user_a):
    # Act
    response = client.get("/cases?page=0")

    # Assert
    assert response.status_code == 422

def test_pagination_invalid_page_size_returns_422(client, user_a):
    # Act
    response = client.get("/cases?page_size=0")

    # Assert
    assert response.status_code == 422

def test_pagination_page_size_above_limit_returns_422(client, user_a):
    # Act
    response = client.get("/cases?page_size=101")

    # Assert
    assert response.status_code == 422


#Sorting tests........................
def test_user_can_sort_cases_by_title_asc(client, user_a):
    titles = ["Bravo", "Alpha", "Charlie"]
    for t in titles:
        response = client.post(
            "/cases",
            json={
                "title": t,
                "description": "sorting test"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?sort_by=title&sort_order=asc")

    assert response.status_code == 200
    data = response.json()
    returned_titles = [item["title"] for item in data["items"]]

    assert returned_titles == sorted(titles)

def test_user_can_sort_cases_by_title_desc(client, user_a):

    titles = ["Bravo", "Alpha", "Charlie"]
    for t in titles:
        response = client.post(
            "/cases",
            json={
                "title": t,
                "description": "sorting test"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?sort_by=title&sort_order=desc")

    assert response.status_code == 200
    data = response.json()
    returned_titles = [item["title"] for item in data["items"]]

    assert returned_titles == sorted(titles, reverse=True)

def test_user_can_sort_cases_by_description_asc(client, user_a):

    descriptions = ["Bravo desc", "Alpha desc", "Charlie desc"]
    for d in descriptions:
        response = client.post(
            "/cases",
            json={
                "title": f"title {d}",
                "description": d
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?sort_by=description&sort_order=asc")

    assert response.status_code == 200
    data = response.json()
    returned_descriptions = [item["description"] for item in data["items"]]

    assert returned_descriptions == sorted(descriptions)

def test_user_can_sort_cases_by_description_desc(client, user_a):

    descriptions = ["Bravo desc", "Alpha desc", "Charlie desc"]
    for d in descriptions:
        response = client.post(
            "/cases",
            json={
                "title": f"title {d}",
                "description": d
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?sort_by=description&sort_order=desc")

    assert response.status_code == 200
    data = response.json()
    returned_descriptions = [item["description"] for item in data["items"]]

    assert returned_descriptions == sorted(descriptions, reverse=True)

def test_sort_by_invalid_field_does_not_crash_and_preserves_insertion_order(client, user_a):

    titles = ["Bravo", "Alpha", "Charlie"]
    for t in titles:
        response = client.post(
            "/cases",
            json={
                "title": t,
                "description": "invalid sort test"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?sort_by=invalid_field&sort_order=asc")

    assert response.status_code == 422


#filtering tests.....................
def test_user_can_filter_cases_by_title(client, user_a):

    titles = ["Alpha", "Bravo", "Charlie"]
    for t in titles:
        response = client.post(
            "/cases",
            json={
                "title": t,
                "description": "filter test"
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?title=r")

    assert response.status_code == 200
    data = response.json()
    returned_titles = [item["title"] for item in data["items"]]

    expected_titles = [t for t in titles if "r" in t.lower()]
    assert set(returned_titles) == set(expected_titles)

def test_user_can_filter_cases_by_description(client, user_a):

    descriptions = ["First Desc", "Second Desc", "Third Desc"]
    for i, d in enumerate(descriptions):
        response = client.post(
            "/cases",
            json={
                "title": f"title {i}",
                "description": d
            }
        )
        assert response.status_code == 201

    response = client.get("/cases?description=ir")

    # 
    assert response.status_code == 200
    data = response.json()
    returned_descriptions = [item["description"] for item in data["items"]]

    assert returned_descriptions == ["First Desc", "Third Desc"]

def test_user_can_filter_cases_by_title_and_description(client, user_a):
    # Arrange: create 3 cases
    cases = [
        {"title": "Alpha", "description": "First Desc"},
        {"title": "Bravo", "description": "Second Desc"},
        {"title": "Alpha", "description": "Third Desc"},
    ]
    for c in cases:
        response = client.post("/cases", json=c)
        assert response.status_code == 201

    # Act: filter title="Alpha" AND description="Third"
    response = client.get("/cases?title=Alpha&description=Third")

    # Assert
    assert response.status_code == 200
    data = response.json()

    # only one case matches both conditions
    assert len(data["items"]) == 1
    assert data["items"][0]["title"] == "Alpha"
    assert data["items"][0]["description"] == "Third Desc"


# filter + sort + pagination integration test.......
def test_filter_sort_pagination_combined(client, user_a):

    cases = [
        {"title": "Alpha", "description": "First Desc"},
        {"title": "Bravo", "description": "Second Desc"},
        {"title": "Alpha", "description": "Third Desc"},
        {"title": "Charlie", "description": "First Desc"},
        {"title": "Alpha", "description": "Second Desc"},
        {"title": "Bravo", "description": "Third Desc"},
    ]
    for c in cases:
        response = client.post("/cases", json=c)
        assert response.status_code == 201

    response = client.get(
        "/cases?title=Alpha&description=Desc&sort_by=title&sort_order=desc&page=1&page_size=2"
    )

    assert response.status_code == 200
    data = response.json()
    
    assert data["page"] == 1
    assert data["page_size"] == 2
    assert data["total"] == 3
    assert len(data["items"]) == 2
    
    for item in data["items"]:
        assert "Alpha" in item["title"]
        assert "Desc".lower() in item["description"].lower()
    
    titles_in_response = [item["title"] for item in data["items"]]
    assert titles_in_response == ["Alpha", "Alpha"]




