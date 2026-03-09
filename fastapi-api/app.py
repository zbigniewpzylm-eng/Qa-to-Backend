from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError, ResponseValidationError
from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional
app = FastAPI()

class CreateUser(BaseModel):
    name: str
    email: EmailStr
    model_config = {"extra": "forbid"}  # zabronione dodatkowe pola

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    model_config = {"extra": "ignore"}  # ignoruj dodatkowe pola w response

class UserUpdate(BaseModel): #PATCH
    #id: int
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    metadata: Optional[dict] = None
    model_config = {"extra": "ignore"}  # ignoruj dodatkowe pola w response

class UserOverWrite(BaseModel): #PUT
    #id: int
    name: str
    email: EmailStr
    model_config = {"extra": "ignore"}  # ignoruj dodatkowe pola w response

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
    """{"id": 1, "name": "Alice", "email": "alice@example.com"},  # poprawny
    {"id": 2, "name": "Bob", "email": "bob@example.com"},      # poprawny
    {"id": 3, "name": "Charlie"},                               # brak email
    {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30},  # extra field
    {"id": 5, "name": "Mallory", "email": "mallory@example.com", "password": "123"},  # extra forbidden"""
]

@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int):
    for user in mock_users:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

# POST USER
@app.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: CreateUser):
    #print("Incoming user:", user)
    #print("Current mock_users IDs:", [u.get("id") for u in mock_users])

    for item in mock_users:
        #if item.get("email") == user.email:
        if item.get("email", "").lower() == user.email.lower():    
            raise HTTPException(status_code=409, detail="Email already exists")

    max_id = max([item.get("id", 0) for item in mock_users], default=0)
    new_id = max_id + 1

    user_dict = user.model_dump()
    user_dict["id"] = new_id

    mock_users.append(user_dict)

    return user_dict
@app.patch("/users/{id}", response_model=UserResponse)
async def update_user(id: int, user: UserUpdate):
    for existing_user in mock_users:
        if id == existing_user["id"]:            
            if user.name is not None:
                existing_user ["name"] = user.name
            if user.email is not None:
                existing_user ["email"] = user.email
            if user.metadata is not None:
                existing_user.update = user.metadata
            return existing_user  
    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{id}", response_model=UserResponse)
async def update_user(user: UserOverWrite):
            for user in mock_users:
                if user["id"] == id:
                    return user
            raise HTTPException(status_code=404, detail="User not found")
