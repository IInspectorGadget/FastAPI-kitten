from src.repositories.breed import BreedRepository


class BreedService:
    def __init__(self, repository: BreedRepository):
        self.repository = repository

    async def list_breeds(self):
        return await self.repository.get_all_breeds()