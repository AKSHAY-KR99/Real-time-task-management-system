from app.database import users_collection
from app.auth.utils import hash_password, verify_password

async def create_user(email: str, password: str, full_name: str = None, role: str = "user"):
    if not role:
        role = "user"

    existing_user = await users_collection.find_one({"email": email})
    if existing_user:
        return None

    user_data = {
        "email": email,
        "password": hash_password(password),
        "full_name": full_name,
        "role": role
    }

    result = await users_collection.insert_one(user_data)
    user_data["id"] = str(result.inserted_id)
    del user_data["password"]
    return user_data



async def authenticate_user(email: str, password: str):
    try:
        user = await users_collection.find_one({"email": email})
        if not user:
            return None

        if not verify_password(password, user["password"]):
            return None

        return user
    except Exception as e:
        print("Auth Service Error:", e)
        return None