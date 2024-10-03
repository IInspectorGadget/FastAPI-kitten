from typing import List

from fastapi import Depends, APIRouter

from src.factory import ServiceFactory, service_factory
from src.schemas.breed import BreedView
from src.services.breed import BreedService

router = APIRouter(tags=['breeds'], prefix='/breeds')


@router.get("/", response_model=List[BreedView], description="Получение списка пород")
async def list_breeds(service: BreedService = Depends(service_factory.create_breed_service)):
    return await service.list_breeds()

