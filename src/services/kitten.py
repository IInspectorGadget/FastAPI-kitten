from typing import List

from fastapi import HTTPException

from src.repositories.kitten import KittenRepository
from src.schemas.kitten import KittenView, KittenCreate, KittenUpdate, KittenPatch


class KittenService:
    def __init__(self, repository: KittenRepository):
        self.repository = repository
        self.view_model = KittenView

    async def list_kittens(self, bread_id: int = None) -> List[KittenView]:
        items = await self.repository.get_all_kittens(bread_id)
        return [self.view_model.model_validate(item, from_attributes=True) for item in items]

    async def get_kitten_by_id(self, kitten_id: int) -> KittenView:
        item = await self.repository.get_kitten_by_id(kitten_id)
        if item is None:
            raise HTTPException(status_code=404, detail="Kitten not found")
        return self.view_model.model_validate(item, from_attributes=True)

    async def create_kitten(self, kitten: KittenCreate) -> KittenView:
        item = await self.repository.add_kitten(kitten)
        return self.view_model.model_validate(item, from_attributes=True)

    async def update_kitten(self, kitten_id: int, kitten_data: KittenUpdate) -> KittenView:
        item = await self.repository.update_kitten(kitten_id, kitten_data)
        if item is None:
            raise HTTPException(status_code=404, detail="Kitten not found")
        return self.view_model.model_validate(item, from_attributes=True)

    async def patch_kitten(self, kitten_id: int, kitten_data: KittenPatch) -> KittenView:
        item = await self.repository.patch_kitten(kitten_id, kitten_data)
        if item is None:
            raise HTTPException(status_code=404, detail="Kitten not found")
        return self.view_model.model_validate(item, from_attributes=True)

    async def delete_kitten(self, kitten_id: int) -> bool:
        deleted = await self.repository.delete_kitten(kitten_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Kitten not found")
        return True

    #
    # async def update_kitten(self, kitten_id: int, **kwargs):
    #     kitten = await self.repository.get_kitten_by_id(kitten_id)
    #     for key, value in kwargs.items():
    #         setattr(kitten, key, value)
    #     await self.repository.update_kitten(kitten)
    #
    # async def delete_kitten(self, kitten_id: int):
    #     kitten = await self.repository.get_kitten_by_id(kitten_id)
    #     await self.repository.delete_kitten(kitten)
