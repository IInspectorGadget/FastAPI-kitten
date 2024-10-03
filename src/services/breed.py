from src.repositories.breed import BreedRepository
from src.schemas.breed import BreedView


class BreedService:
    def __init__(self, repository: BreedRepository):
        self.repository = repository

    async def list_breeds(self) -> BreedView:
        return await self.repository.get_all_breeds()
