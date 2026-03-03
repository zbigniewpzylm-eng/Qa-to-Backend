import pytest
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_get_existing_user_returns_200():
    response = client.get("/users/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Alice", "email": "alice@example.com"}

def test_get_non_existing_user_returns_404():
    response = client.get("/users/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"

def test_get_invalid_input_returns_422():
    response = client.get("/users/abc")
    data = response.json()
    assert response.status_code == 422
    assert data["detail"][0]["loc"] == ["path", "id"]
    assert "Input should be a valid integer" in data["detail"][0]["msg"]


def test_get_missing_optional_data_returns_200():
    # Upewnić sie ze user 8 istnieje ale brak w nim emaila
    response = client.get("/users/8")    
    assert response.status_code == 200
    assert response.json() ==  {"id": 8, "name": "Trudy", 'email': None}

def test_get_additional_forbiden_data_returns_500():
    # Upewnić sie ze user 5 istnieje i ma dodatkowe pola
    response = client.get("/users/5")    
    assert response.status_code == 422
    #assert response.json()["detail"] == "Internal Server Error"


'''
Do parametryzacji TC: 1, 2, 7,


TC1 — Existing user!
Input: /users/1
Expected status: 200
Expected body: poprawny JSON zgodny z modelem

TC2 — Non-Existing user!
Input: /users/999
Expected status: 404
Expected body: User not found

TC3 — Existing user aditional fields in return JSON - fields permited but not returned
Input: /users/3
Expected status: 200
Expected body: poprawny JSON zgodny z modelem

TC4 — Existing user aditional fields in return JSON -  optional fields permited and returned
Input: /users/4
Expected status: 200
Expected body: poprawny JSON zgodny z modelem

TC5 — Existing user aditional fields in return JSON -  optional fields not permited!
Input: /users/5
Expected status: 500
Expected body: Internal Server Error - Data niezgodna z modelem

TC6 — Existing user - timeout
Input: /users/1 - timeout
Expected status: 500
Expected body: Internal Server Error - timeout

TC7 — Invalid input
Input: /users/abc
Expected status: 422
Expected body: Nieprzetwarzalny Żądanie

TC8 — Existing user - Missing data - Restrictive!
Input: /users/8 
Expected status: 500
Expected body: Internal Server Error 

TC9 — Existing user - Missing data - Optional
Input: /users/9 
Expected status: 200
Expected body: poprawny JSON zgodny z modelem (puste pola zwrócone jako puste)














'''