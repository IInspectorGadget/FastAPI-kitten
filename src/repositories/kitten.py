from contextlib import AbstractContextManager
from typing import Callable, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session, joinedload

from src.models import Kitten
from src.schemas.kitten import KittenView, KittenCreate, KittenUpdate, KittenPatch


class KittenRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        self.model = Kitten
        self.base_stmt = select(Kitten).options(joinedload(self.model.breed))

    async def get_all_kittens(self, bread_id: int) -> List[Kitten]:
        async with self.session_factory() as session:
            stmt = self.base_stmt
            if bread_id:
                stmt = stmt.filter(self.model.breed_id == bread_id)
            result = await session.execute(stmt)
            items = result.scalars().all()
            return items

    async def get_kitten_by_id(self, kitten_id: int):
        async with self.session_factory() as session:
            query = self.base_stmt.where(Kitten.id == kitten_id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    async def add_kitten(self, kitten_data: KittenCreate):
        async with self.session_factory() as session:
            async with session.begin():
                kitten = self.model(**kitten_data.model_dump())
                session.add(kitten)
                await session.commit()
            await session.refresh(kitten, attribute_names=['breed'])
            return kitten

    async def update_kitten(self, kitten_id: int, kitten_data: KittenUpdate):
        async with self.session_factory() as session:
            async with session.begin():
                kitten = await session.get(self.model, kitten_id)
                if not kitten:
                    return None
                for key, value in kitten_data.model_dump().items():
                    setattr(kitten, key, value)
                await session.commit()
            await session.refresh(kitten, attribute_names=['breed'])
            return kitten

    async def patch_kitten(self, kitten_id: int, kitten_data: KittenPatch):
        async with self.session_factory() as session:
            async with session.begin():
                kitten = await session.get(self.model, kitten_id)
                if not kitten:
                    return None
                for key, value in kitten_data.model_dump(exclude_unset=True).items():
                    setattr(kitten, key, value)
                await session.commit()
            await session.refresh(kitten, attribute_names=['breed'])
            return kitten

    async def delete_kitten(self, kitten_id: int) -> bool:
        async with self.session_factory() as session:
            async with session.begin():
                kitten = await session.get(self.model, kitten_id)
                if not kitten:
                    return False
                await session.delete(kitten)
                await session.commit()
            return True
