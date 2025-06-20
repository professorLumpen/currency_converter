from fastapi import FastAPI

from app.api.endpoints.users import user_router


app = FastAPI()
app.include_router(user_router)
