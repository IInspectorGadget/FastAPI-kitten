from functools import lru_cache
from typing import TypeVar

from dotenv import load_dotenv
from pydantic import PostgresDsn, BaseModel, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
load_dotenv()
TSettings = TypeVar("TSettings", bound=BaseSettings)


class PostgresSettings(BaseModel):
    scheme: str
    user: str
    password: str
    host: str
    port: str
    db: str
    url: PostgresDsn | None = None

    @model_validator(mode="after")
    def set_postgres_dsn(self):
        if not self.url:
            self.url = PostgresDsn(
                f"{self.scheme}://"
                f"{self.user}:"
                f"{self.password}@"
                f"{self.host}:"
                f"{self.port}/"
                f"{self.db if self.db else 'postgres'}"
            )
        return self


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        extra="allow",
        env_nested_delimiter="__",
    )
    postgres: PostgresSettings


@lru_cache
def get_settings(cls: type[TSettings]) -> TSettings:
    return cls()
