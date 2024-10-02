from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel

from src.schemas.breed import BreedView


class KittenBase(BaseModel):
    color: str
    age: int
    description: str
    breed_id: int

    class Config:
        from_attributes = True
        populate_by_name = True
        alias_generator = to_camel


class KittenCreate(KittenBase):
    pass


class KittenUpdate(KittenBase):
    pass


class KittenPatch(KittenBase):
    color: str | None = Field(None)
    age: int | None = Field(None)
    description: str | None = Field(None)
    breed_id: int | None = Field(None)


class KittenView(KittenBase):
    id: int
    breed: BreedView
