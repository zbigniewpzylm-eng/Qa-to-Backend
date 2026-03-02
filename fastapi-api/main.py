from fastapi import FastAPI
from fastapi import HTTPException
from pydantic import BaseModel

app = FastAPI()

class User(BaseModel):
    id: int
    name: str
    email: str | None = None

    model_config = {
        "extra": "forbid"
    }


mock_users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Bob",},
    {"id": 4, "name": "Eve", "email": "eve@example.com", "age": 30}
]

@app.get("/users/{id}", response_model=User)
async def get_user(id: int):
    for user in mock_users:
        if user["id"] == id:
            return user

    raise HTTPException(status_code=404, detail="User not found")


    
    
    
   