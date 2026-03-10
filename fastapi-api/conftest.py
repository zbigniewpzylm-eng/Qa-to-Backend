import pytest
from app import mock_users, app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_mock_users():
    mock_users.clear()
    mock_users.extend([
        {"id": 1, "name": "Alice", "email": "alice@example.com"},
        {"id": 2, "name": "Bob", "email": "bob@example.com"},
        #{"id": 3, "name": "Bob"},  # brak email
        {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30},  # extra field
        {"id": 5, "name": "Mallory", "email": "mallory@example.com", "password": "123"},
        #{"id": 8, "name": "Trudy"}  # brak email
    ])