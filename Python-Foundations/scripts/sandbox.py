class InvalidApiResponseError(Exception):
    """Custom exception for invalid API responses"""
    pass

def parse_data(data):
    if not isinstance(data, (dict, list)): #sprawdzam czy input który dostałem jest takiego typu jaki mnie interesuje.
        raise InvalidApiResponseError("Input data must be a dictionary or a list") #podnosze błąd jeśli nie jest jednym z dwóch podanych typów

    if isinstance(data, dict):
        data = [data] #upewniam sie ze input jest ujednoliconym typem danych

    required_keys = ['first', 'second'] #lista kluczy które muszą sie znaleźć żeby input był prawidłowy

    for obj in data: #ze wszystkich obiektów w inpucie
        for key in required_keys: #sprawdzamy każdy klucz z wymaganych kluczy
            if key not in obj: #jeżeli klucz z wymaganych kluczy nie pojawia sie w kluczach z inputu
                raise InvalidApiResponseError(f"Missing required key '{key}' in object: {obj}") #podnosze error żeby poinformować że brakuje odpowiedniego klucza
    
    result = [{k: obj[k] for k in required_keys} for obj in data]

    return result



