from schemas.user import UserCreate


def test_user_can_register_and_login(client):
    
    #regiser test
    user = UserCreate(
        username="test user",
        password="user password",
         role="user"
    )

    register_response = client.post("/register" , json=user.model_dump())
    assert register_response.status_code == 201

    data_register = register_response.json()
    assert data_register["username"] == "test user"
    assert data_register["role"] == "user"
    assert "password" not in data_register
    assert "id" in data_register


    #login test
    login_data = {"username":"test user" , "password":"user password"}
    login_reponse = client.post("/login", data=login_data )
    assert login_reponse.status_code == 200

    data_login = login_reponse.json()
    assert data_login["access_token"] != None
    assert data_login["token_type"]== "bearer"

def test_admin_can_register_and_login(client):
    
    #regiser test
    user = UserCreate(
        username="test admin",
        password="admin password",
         role="admin"
    )

    response = client.post("/register" , json=user.model_dump())
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == "test admin"
    assert data["role"] == "admin"
    assert "password" not in data
    assert "id" in data
    
    #login test
    login_data = {"username":"test admin" , "password":"admin password"}
    login_reponse = client.post("/login", data=login_data )
    assert login_reponse.status_code == 200

    data_login = login_reponse.json()
    assert data_login["access_token"] != None
    assert data_login["token_type"]== "bearer"

def test_non_exist_user_cannot_login(client):

    login_data = {
        "username":"non exist",
        "password":"1234"
    }
    login_response = client.post("/login", data = login_data)
    assert login_response.status_code == 400

def test_duplicate_username_cannot_register(client):

    user1 = UserCreate(
        username="test user",
        password="user1 password",
         role="user"
    )
    user2 = UserCreate(
        username="test user",
        password="user2 password",
         role="user"
    )
    register_response1 = client.post("/register" , json=user1.model_dump())
    assert register_response1.status_code == 201

    register_response2 = client.post("/register" , json=user2.model_dump())
    assert register_response2.status_code == 400













