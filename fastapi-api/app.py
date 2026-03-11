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

class UserUpdateResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    metadata: Optional[dict] = None
    model_config = {"extra": "allow"}  # żeby przyszłe dodatkowe pola też mogły się pokazać


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
    {"id": 1, "name": "Alice", "email": "alice@example.com"},  # poprawny
    {"id": 2, "name": "Bob", "email": "bob@example.com"},      # poprawny
    {"id": 3, "name": "Charlie"},                               # brak email
    {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30},  # extra field
    {"id": 5, "name": "Mallory", "email": "mallory@example.com", "password": "123"},  # extra forbidden
]

@app.get("/users/{id}", response_model=UserResponse)
async def get_user(id: int):
    for user in mock_users:
        if user["id"] == id:
            return user
    raise HTTPException(status_code=404, detail="User not found")

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
@app.patch("/users/{id}", response_model=UserUpdateResponse)
async def update_user(id: int, user: UserUpdate):

    update_data = user.model_dump(exclude_unset=True)

    if "email" in update_data:
        update_data["email"] = update_data["email"].lower()

    for existing_user in mock_users:

        if existing_user["id"] == id:

            if "email" in update_data:

                new_email = update_data["email"].lower()
                current_email = existing_user.get("email")

                if current_email and new_email != current_email.lower():

                    for mock_user in mock_users:
                        email = mock_user.get("email")

                        if email and email.lower() == new_email and mock_user["id"] != id:
                            raise HTTPException(
                                status_code=409,
                                detail="Email already exists"
                            )

            if "metadata" in update_data:

                existing_metadata = existing_user.get("metadata", {})
                existing_metadata.update(update_data["metadata"])

                existing_user["metadata"] = existing_metadata
                update_data.pop("metadata")

            existing_user.update(update_data)

            return existing_user

    raise HTTPException(status_code=404, detail="User not found")


@app.put("/users/{id}", response_model=UserResponse)
async def overwrite_user(id: int, user: UserOverWrite):




    for existing_user in mock_users:

        if existing_user["id"] == id:

            # duplicate email check
            for u in mock_users:

                email = u.get("email")

                if email and email.lower() == user.email.lower() and u["id"] != id:
                    raise HTTPException(status_code=409, detail="Email already exists")

            existing_user["name"] = user.name
            existing_user["email"] = user.email

            # usuń metadata jeśli było wcześniej
            existing_user.pop("metadata", None)

            return existing_user

    raise HTTPException(status_code=404, detail="User not found")

@app.delete("/users/{id}", status_code=204)
async def delete_user(id: int):

    for user in mock_users:

        if user["id"] == id:
            mock_users.remove(user)
            return

    raise HTTPException(status_code=404, detail="User not found")