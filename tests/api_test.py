import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from contextlib import asynccontextmanager

from src.application import app
from src.database import Database
from src.factory import service_factory
from src.models import Base, Breed, Kitten
from src.repositories.breed import BreedRepository
from src.repositories.kitten import KittenRepository
from src.services.breed import BreedService
from src.services.kitten import KittenService

class TestDatabase:
    def __init__(self, db_url: str = "sqlite+aiosqlite:///:memory:"):
        self._engine = create_async_engine(db_url, echo=True)
        self._session_factory = async_sessionmaker(
            autocommit=False,
            autoflush=False,
            bind=self._engine,
        )

    async def create_database(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def clear_database(self):
        async with self._engine.begin() as conn:
            # Удаляем данные из всех таблиц
            for table in reversed(Base.metadata.sorted_tables):
                await conn.execute(table.delete())

    @asynccontextmanager
    async def session(self) -> AsyncSession:
        session: AsyncSession = self._session_factory()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@pytest_asyncio.fixture(scope="function")
async def test_db():
    test_database = TestDatabase()
    await test_database.create_database()
    await test_database.clear_database()
    yield test_database


@pytest_asyncio.fixture(scope="function")
async def breed(test_db):
    async with test_db.session() as session:
        new_breed = Breed(name="Siamese")
        session.add(new_breed)
        await session.commit()
        await session.refresh(new_breed)
        yield new_breed


@pytest_asyncio.fixture(scope="function")
async def kitten(test_db, breed):
    async with test_db.session() as session:
        new_breed = Kitten(description="Fluffy", color="black", age=1, breed_id=breed.id)
        session.add(new_breed)
        await session.commit()
        await session.refresh(new_breed)
        yield new_breed


@pytest_asyncio.fixture(scope="function")
async def async_client(test_db):
    async def override_create_kitten_service():
        repository = KittenRepository(test_db.session)
        return KittenService(repository)

    async def override_create_breed_service():
        repository = BreedRepository(test_db.session)
        return BreedService(repository)

    app.dependency_overrides[service_factory.create_kitten_service] = override_create_kitten_service
    app.dependency_overrides[service_factory.create_breed_service] = override_create_breed_service
    app.dependency_overrides[Database.session] = lambda: test_db.session()
    app.dependency_overrides[Database] = lambda: test_db

    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_create_kitten(async_client, breed):
    response = await async_client.post("/kittens/", json={"description": "Fluffy", "color": "black", "age": 1, "breed_id": breed.id})
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Fluffy"
    assert data["color"] == "black"
    assert data["breed"]["id"] == breed.id


@pytest.mark.asyncio
async def test_list_kittens(async_client, kitten):
    response = await async_client.get("/kittens/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == kitten.id


@pytest.mark.asyncio
async def test_list_kittens_with_filter(async_client, kitten):
    response = await async_client.get(f'/kittens/?breed_id={kitten.breed_id}')
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == kitten.id


@pytest.mark.asyncio
async def test_update_kitten(async_client, kitten):
    update_data = {"description": "Mittens", "age": 2}
    response = await async_client.patch(f"/kittens/{kitten.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Mittens"
    assert data["age"] == 2


@pytest.mark.asyncio
async def test_update_kitten(async_client, kitten):
    update_data = {"description": "Mittens", "age": 2, "color": "white", "breed_id": kitten.breed_id}
    response = await async_client.put(f"/kittens/{kitten.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Mittens"
    assert data["age"] == 2
    assert data["color"] == "white"


@pytest.mark.asyncio
async def test_delete_kitten(async_client, kitten):
    response = await async_client.delete(f"/kittens/{kitten.id}")
    assert response.status_code == 200
    response = await async_client.get(f"/kittens/{kitten.id}")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_list_breeds(async_client, breed):
    # Проверяем, что котенок был добавлен
    response = await async_client.get("/breeds/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == breed.id
