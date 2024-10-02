from src.database import Database
from src.repositories.breed import BreedRepository
from src.repositories.kitten import KittenRepository
from src.services.breed import BreedService
from src.services.kitten import KittenService
from src.settings import Settings, get_settings


class ServiceFactory:
    def __init__(self):
        self._db = Database(str(get_settings(Settings).postgres.url))

    async def create_kitten_service(self) -> KittenService:
            repository = KittenRepository(self._db.session)
            return KittenService(repository)

    async def create_breed_service(self) -> BreedService:
            repository = BreedRepository(self._db.session)
            return BreedService(repository)


service_factory = ServiceFactory()

