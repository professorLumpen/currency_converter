from fastapi.params import Depends
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.db.database import get_async_session
from app.db.models import User
from app.repositories.base_repository import Repository


class UserRepository(Repository):
    model = User


async def get_user_repository(session: AsyncSession = Depends(get_async_session)) -> UserRepository:
    user_repository = UserRepository(session)
    return user_repository
