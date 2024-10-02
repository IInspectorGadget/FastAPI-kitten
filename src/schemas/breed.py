from pydantic import BaseModel


class BreedBase(BaseModel):
    name: str


class BreedView(BreedBase):
    id: int

    class Config:
        from_attributes = True