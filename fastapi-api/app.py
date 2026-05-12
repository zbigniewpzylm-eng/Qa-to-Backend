from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from routes import router
app = FastAPI()

app.include_router(router)



@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )

mock_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},  # poprawny
    {"id": 2, "name": "Bob", "email": "bob@example.com"},      # poprawny
    {"id": 3, "name": "Charlie"},                               # brak email
    {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30},  # extra field
    {"id": 5, "name": "Mallory", "email": "mallory@example.com", "password": "123"},  # extra forbidden
]


