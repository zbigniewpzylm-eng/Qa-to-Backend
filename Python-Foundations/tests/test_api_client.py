import pytest
from scripts.api_client import fetch_user, requests, InvalidApiResponseError




def test_fetch_user_success(mocker):
    # Tworzymy "mock" odpowiedzi z API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }

    mocker.patch("requests.get", return_value=mock_response)

    result = fetch_user(1)

    # Sprawdzamy wynik
    assert result["id"] == 1
    assert result["name"] == "Alice"
    assert result["email"] == "alice@example.com"


def test_fetch_invalid_user_to_float(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1.5 ,
        "name": "Alice",
        "email": "alice@example.com"
    }

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_fetch_invalid_name_not_sting(mocker):
    # Tworzymy "mock" odpowiedzi z API
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": 1,
        "name": ["Alice"],
        "email": "alice@example.com"
    }

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_fetch_user_invalid_status(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404  # zły status
    mock_response.json.return_value = {}

    mocker.patch("requests.get", return_value=mock_response)

    # Funkcja powinna podnieść nasz custom exception
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_fetch_user_missing_keys(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"id": 1, "name": "Alice"}  # brak 'email'

    mocker.patch("requests.get", return_value=mock_response)

    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_fetch_user_timeout(mocker):

    mocker.patch(
        "requests.get",
        side_effect=requests.exceptions.ReadTimeout
    )


    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)


def test_invalid_user_not_int():
    with pytest.raises(InvalidApiResponseError):
        fetch_user("abc")

def test_invalid_json_not_dict(mocker):
    json_list_response = {
    "status_code": 200,
    "json": lambda: [{"id": 1, "name": "Alice"}]  
}
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = json_list_response

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_invalid_id_not_int(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "1",
        "name": "Alice",
        "email": "alice@example.com"
    }

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_invalid_name_not_string(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "1",
        "name": 1,
        "email": "alice@example.com"
    }

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)

def test_invalid_email_incorrect(mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "1",
        "name": ["Alice"],
        "email": 1
    }

    # Zastępujemy requests.get naszym mockiem
    mocker.patch("requests.get", return_value=mock_response)


    # Sprawdzamy wynik
    with pytest.raises(InvalidApiResponseError):
        fetch_user(1)



