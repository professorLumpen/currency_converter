from abc import ABC, abstractmethod

from fastapi import HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio.session import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def find_one(self, data: dict):
        pass

    @abstractmethod
    async def find_all(self):
        pass

    @abstractmethod
    async def add_one(self, data: dict):
        pass

    @abstractmethod
    async def delete_one(self, data: dict):
        pass

    @abstractmethod
    async def update_one(self, filter_data: dict, update_data: dict):
        pass


class Repository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def find_one(self, data: dict):
        conditions = [getattr(self.model, key) == val for key, val in data.items()]

        query = select(self.model).where(and_(*conditions))
        result = await self.session.execute(query)
        obj = result.scalar_one_or_none()

        if not obj:
            raise HTTPException(status_code=404, detail="Object not found")

        return obj

    async def find_all(self):
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def add_one(self, data: dict):
        obj = await self.find_one(data)
        if obj:
            raise HTTPException(401, "Object already exists")

        new_obj = self.model(**data)
        self.session.add(new_obj)
        await self.session.commit()
        await self.session.refresh(new_obj)

        return new_obj

    async def delete_one(self, data: dict):
        obj = await self.find_one(data)

        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True

        return False

    async def update_one(self, filter_data: dict, update_data: dict):
        obj = await self.find_one(filter_data)

        if obj:
            for key, value in update_data.items():
                setattr(obj, key, value)

            await self.session.commit()
            await self.session.refresh(obj)
            return obj

        return False
