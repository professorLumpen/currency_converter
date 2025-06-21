from fastapi import APIRouter, Depends, HTTPException

from app.api.schemas.users import Token, UserCreate, UserFromDB, UserLogin
from app.core.security import create_access_token, get_password_hash, verify_password
from app.repositories.user_repository import UserRepository, get_user_repository


user_router = APIRouter(prefix="/auth", tags=["auth"])


@user_router.post("/register/", response_model=UserFromDB)
async def register(user_data: UserCreate, user_repo: UserRepository = Depends(get_user_repository)) -> UserFromDB:
    user_dict = user_data.model_dump()
    user_dict["password"] = get_password_hash(user_dict["password"])

    user_from_db = await user_repo.add_one(user_dict)
    user_to_return = UserFromDB.model_validate(user_from_db)

    return user_to_return


@user_router.post("/login/", response_model=Token)
async def login(user_data: UserLogin, user_repo: UserRepository = Depends(get_user_repository)):
    user_from_db = await user_repo.find_one({"username": user_data.username})

    if verify_password(user_data.password, user_from_db.password):
        payload_data = {"sub": str(user_from_db.id)}
        return {"token": create_access_token(payload_data)}

    raise HTTPException(status_code=401, detail="Incorrect username or password")
