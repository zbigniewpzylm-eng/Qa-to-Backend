from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.exceptions import ResponseValidationError
from pydantic import BaseModel
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import RequestValidationError

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str | None = None

    model_config = {
        "extra": "forbid"
    }
@app.exception_handler(ResponseValidationError)
async def response_validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()},
    )
mock_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Bob"},  # missing email, optional
    {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30},  # extra field age → should fail if extra=forbid
    {"id": 5, "name": "Mallory", "email": "mallory@example.com", "password": "123"},  # extra forbidden
    {"id": 8, "name": "Trudy"}  # missing required field
]


@app.get("/users/{id}", response_model=User)
async def get_user(id: int):
    for user in mock_users:
        if user["id"] == id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


    
    
    
   