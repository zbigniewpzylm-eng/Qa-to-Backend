import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)
@pytest.mark.get
def test_get_existing_user_returns_200():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "email": "alice@example.com"}
@pytest.mark.get
def test_get_non_existing_user_returns_404():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
@pytest.mark.get
def test_get_invalid_input_returns_422():
    response = client.get("/users/abc")
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["path", "id"]
    assert "Input should be a valid integer" in data["detail"][0]["msg"]

@pytest.mark.get
def test_get_missing_optional_data_returns_200():
    # Upewnić sie ze user 8 istnieje ale brak w nim emaila
    response = client.get("/users/8")    
    assert response.status_code == 200
    assert response.json() ==  {"id": 8, "name": "Trudy", 'email': None}
@pytest.mark.get
def test_get_additional_forbiden_data_returns_500():
    # Upewnić sie ze user 5 istnieje i ma dodatkowe pola
    response = client.get("/users/5")    
    assert response.status_code == 422
    assert "extra fields" in response.json()["detail"][0]["msg"].lower()

@pytest.mark.post
def test_post_user_created_return_201():
    response = client.post("/users/", json= {
  "name": "string",
  "email": "user@example.com"
})
    data = response.json()

    assert "id" in data
    assert isinstance(data["id"], int)
    assert data["name"] == "string"
    assert data["email"] == "user@example.com"

@pytest.mark.post
def test_post_duplicate_user_created_return_409():


    client.post("/users/", json={
        "name": "string",
        "email": "dup@example.com"
    })
    response = client.post("/users/", json={
        "name": "string",
        "email": "dup@example.com"
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.post
def test_post_missing_email_return_422():
    response = client.post("/users/", json= {
  "name": "string",
  
})
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "email"  
    assert data["detail"][0]["msg"] == "Field required"

@pytest.mark.post
def test_post_missing_name_return_422():
    response = client.post("/users/", json= {
  "email": "dup@example.com",
  
})
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "name"  
    assert data["detail"][0]["msg"] == "Field required"


@pytest.mark.post
def test_post_additional_field_return_422():
    response = client.post("/users/", json= {
  "name": "string",
  "email": "dup@example.com",
  "age": 20

  
})
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "age"
    assert "extra inputs are not permitted" in data["detail"][0]["msg"].lower()

















