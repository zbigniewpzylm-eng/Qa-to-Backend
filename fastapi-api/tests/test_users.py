import pytest
from  conftest import client
from app import app 


@pytest.mark.get
def test_get_existing_user_returns_200(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "email": "alice@example.com"}
@pytest.mark.get
def test_get_non_existing_user_returns_404(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
@pytest.mark.get
def test_get_invalid_input_returns_422(client):
    response = client.get("/users/abc")
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["path", "id"]
    assert "Input should be a valid integer" in data["detail"][0]["msg"]

@pytest.mark.get
def test_get_missing_optional_data_returns_200(client):
    # Upewnić sie ze user 8 istnieje ale brak w nim emaila
    response = client.get("/users/")    
    assert response.status_code == 200
    assert response.json() ==  {"id": 8, "name": "Trudy", 'email': None}
@pytest.mark.get
def test_get_additional_forbiden_data_returns_500(client):
    # Upewnić sie ze user 5 istnieje i ma dodatkowe pola
    response = client.get("/users/5")    
    assert response.status_code == 422
    assert "extra fields" in response.json()["detail"][0]["msg"].lower()

@pytest.mark.post
def test_post_user_created_return_201(client):
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
def test_post_duplicate_user_created_return_409(client):


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
def test_post_missing_email_return_422(client):
    response = client.post("/users/", json= {
  "name": "string",
  
})
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "email"  
    assert data["detail"][0]["msg"] == "Field required"

@pytest.mark.post
def test_post_missing_name_return_422(client):
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




@pytest.mark.patch
def test_patch_update_name_200(client):

    response = client.patch(
        "/users/1",
        json={"name": "Adam"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Adam"
    assert data["email"] == "alice@example.com"

@pytest.mark.patch
def test_patch_update_email_200(client):

    response = client.patch(
        "/users/1",
        json={"email": "test@example.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Alice"
    assert data["email"] == "test@example.com"

@pytest.mark.patch
def test_patch_update_duplicate_email_409(client):

    response = client.patch(
        "/users/1",
        json={"email": "BOB@example.com"}
    )
    data = response.json()
    assert response.status_code == 409    
    assert data["detail"] == "Email already exists"

@pytest.mark.patch
def test_patch_metadata_merge_200(client):

    client.patch("/users/1", json={
        "metadata": {
    "City": "Warsaw"
  }
    })
    response = client.patch("/users/1", json={
        "metadata": {
    "Favorite Band": "Black Sabbath"
  }
    }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["metadata"]["City"] == "Warsaw"
    assert data["metadata"]["Favorite Band"] == "Black Sabbath"    

@pytest.mark.patch
def test_patch_non_existing_user_returns_404(client):
    response = client.patch(
        "/users/999",
        json={"email": "BOB@example.com"}
    )
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

@pytest.mark.put
def test_put_userOverwrite_returns_204(client):
    response = client.put(
        "/users/1",
        json={"name": "Adam",
              "email":"adam@test.com"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["name"] == "Adam"
    assert data["email"] == "adam@test.com"

@pytest.mark.put
def test_put_userOverwrite_missing_email_returns_422(client):
    response = client.put(
        "/users/1",
        json={"name": "Adam",
              }
    )

    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "email"  
    assert data["detail"][0]["msg"] == "Field required"

@pytest.mark.put
def test_put_userOverwrite_missing_name_returns_422(client):
    response = client.put(
        "/users/1",
        json={
              "email":"adam@test.com"}
    )

    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"][-1] == "name"  
    assert data["detail"][0]["msg"] == "Field required"


@pytest.mark.put
def test_put_duplicate_email_created_return_409(client):

    client.put("/users/1", json={
        "name": "adam",
        "email": "dup@example.com"
    })
    response = client.put("/users/2", json={
        "name": "tom",
        "email": "dup@example.com"
    })

    assert response.status_code == 409
    assert response.json()["detail"] == "Email already exists"

@pytest.mark.delete
def test_delete_user_returns_209(client):
    response = client.delete("/users/1")

    assert response.status_code == 209

@pytest.mark.delete
def test_delete_userNotFound_returns_404(client):
    response = client.delete("/users/1")

    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"