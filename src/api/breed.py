from fastapi import Depends, APIRouter

from src.factory import ServiceFactory, service_factory
from src.services.breed import BreedService

router = APIRouter(tags=['breeds'], prefix='/breeds')

# Dependency для получения сессии
@router.get("/")
async def list_breeds(service: BreedService = Depends(service_factory.create_breed_service)):
    return await service.list_breeds()

