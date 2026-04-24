from pydantic import BaseModel
from pydantic import EmailStr
from typing import Optional






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


class UserOverWrite(BaseModel):
    
    #id: int
    name: str
    email: EmailStr
    model_config = {"extra": "ignore"}  # ignoruj dodatkowe pola w response #PUT