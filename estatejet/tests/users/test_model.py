from fastapi.testclient import TestClient


def test_create_user(client: TestClient):
    response = client.post(
        "/users/",
        json={
            "email": "admin@gmail.com",
            "first_name": "First",
            "last_name": "Last",
            "phone_number": "+919092995525",
            "role": "ADMIN",
            "password": "PASSWORD"
        }
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "admin@gmail.com"
    assert "uuid" in data
