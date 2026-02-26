import requests

class InvalidApiResponseError(Exception):
    pass

def fetch_user(user_id: int) -> dict:
    # Walidacja argumentu
    if not isinstance(user_id, int):
        raise InvalidApiResponseError("User id must be an int")

    # Wywołanie API
    try:
        r = requests.get(f"https://example.com/api/users/{user_id}", timeout=3)
        r.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise InvalidApiResponseError("API request failed") from e




    
    # Sprawdzenie statusu HTTP

      
    # Parsowanie JSON
    data = r.json()
    if not isinstance(data, dict):
        raise InvalidApiResponseError("Invalid API Response - Response object is not a dictionary")

    # Wymagane pola
    required_fields = ["id", "name", "email"]
    for key in required_fields:
        if key not in data:
            raise InvalidApiResponseError(f"Missing required key '{key}'")
  
    if not isinstance(data["id"], int):
        raise InvalidApiResponseError(
        f"Invalid 'id' format: {data['id']} (expected int)"
    )

    if not isinstance(data["name"], str):
        raise InvalidApiResponseError("Invalid 'name' format. Expected string.")


    return {"id": data["id"], "name": data["name"], "email": data["email"]}
