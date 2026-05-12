import schemas
from app import mock_users, HTTPException





async def get_user(id: int):
    for user in mock_users:
        if user["id"] == id:
            return user
    raise ValueError("User not found")

async def create_user(user: schemas.CreateUser):


    for item in mock_users:
        #if item.get("email") == user.email:
        if item.get("email", "").lower() == user.email.lower():    
            raise ValueError("Email already exists")

    max_id = max([item.get("id", 0) for item in mock_users], default=0)
    new_id = max_id + 1

    user_dict = user.model_dump()
    user_dict["id"] = new_id

    mock_users.append(user_dict)

    return user_dict
async def update_user(id: int, user: schemas.UserUpdate):

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


async def overwrite_user(id: int, user: schemas.UserOverWrite):




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

async def delete_user(id: int):

    for user in mock_users:

        if user["id"] == id:
            mock_users.remove(user)
            return

    raise HTTPException(status_code=404, detail="User not found")