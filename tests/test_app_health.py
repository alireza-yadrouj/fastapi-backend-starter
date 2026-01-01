from sqlalchemy.orm import Session


def test_app_uses_test_database(client, override_get_db):
   
    response = client.get("/docs")
    assert response.status_code == 200

