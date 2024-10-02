from typing import Optional, List

from fastapi import Depends, APIRouter, Query, HTTPException

from src.factory import ServiceFactory, service_factory
from src.schemas.kitten import KittenView, KittenCreate, KittenUpdate, KittenPatch
from src.services.kitten import KittenService

router = APIRouter(tags=['kittens'], prefix='/kittens')


@router.get("/", response_model=List[KittenView])
async def list_kittens(
    breed_id: Optional[int] = Query(None, description="ID породы для фильтрации"),
    service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.list_kittens(breed_id)


@router.get("/{kitten_id}", response_model=KittenView)
async def get_kitten(
        kitten_id: int,
        service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.get_kitten_by_id(kitten_id)


@router.post("/", response_model=KittenView)
async def create_kitten(
        kitten: KittenCreate,
        service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.create_kitten(kitten)


@router.put("/{kitten_id}", response_model=KittenView)
async def update_kitten(
    kitten_id: int,
    kitten_data: KittenUpdate,
    service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.update_kitten(kitten_id, kitten_data)


@router.patch("/{kitten_id}", response_model=KittenView)
async def patch_kitten(
    kitten_id: int,
    kitten_data: KittenPatch,
    service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.patch_kitten(kitten_id, kitten_data)

@router.delete("/{kitten_id}")
async def delete_kitten(
    kitten_id: int,
    service: KittenService = Depends(service_factory.create_kitten_service)
):
    return await service.delete_kitten(kitten_id)