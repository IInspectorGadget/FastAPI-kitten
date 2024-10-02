from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.database import Base


class Breed(Base):
    __tablename__ = 'breeds'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[int] = mapped_column(String, index=True, unique=True)
    kittens = relationship("Kitten", back_populates="breed")


class Kitten(Base):
    __tablename__ = 'kittens'
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    color: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    description: Mapped[str] = mapped_column(String)
    breed_id: Mapped[int] = mapped_column(Integer, ForeignKey('breeds.id'))
    breed = relationship("Breed", back_populates="kittens")
