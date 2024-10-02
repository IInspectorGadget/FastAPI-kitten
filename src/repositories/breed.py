from contextlib import AbstractContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from src.models import Kitten, Breed
from src.schemas.breed import BreedView
from src.schemas.kitten import KittenView, KittenCreate


class BreedRepository:
    def __init__(self, session_factory: Callable[..., AbstractContextManager[Session]]):
        self.session_factory = session_factory
        self.view_model = BreedView
        self.model = Breed

    async def get_all_breeds(self):
        async with self.session_factory() as session:
            query = select(self.model)
            result = await session.execute(query)
            return result.scalars().all()
