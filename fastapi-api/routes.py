from fastapi import APIRouter, HTTPException
import schemas
import services

router = APIRouter(prefix="/users", tags=["users"])



#
@router.get("/{id}", response_model=schemas.UserResponse)
async def get_user(id: int):
    return await services.get_user(id) #get
@router.post("", response_model=schemas.UserResponse, status_code=201)
async def create_user(user: schemas.CreateUser):
    try:
        return await services.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

@router.patch("/{id}", response_model=schemas.UserUpdateResponse)
async def update_user(id: int, user: schemas.UserUpdate):
    return await services.update_user(id, user)

@router.put("/{id}", response_model=schemas.UserResponse)
async def overwrite_user(id: int, user: schemas.UserOverWrite):
    return await services.overwrite_user(id, user)

@router.delete("/{id}", status_code=204)
async def delete_user(id: int):
    await services.delete_user(id) 