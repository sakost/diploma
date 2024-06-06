from __future__ import annotations

from pydantic_settings import BaseSettings
from sqlalchemy.engine.url import URL


ASYNC_DRIVER_NAME = "postgresql+asyncpg"
SYNC_DRIVER_NAME = "postgresql"


class CustomBaseSettings(BaseSettings):
    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


class DatabaseSettings(CustomBaseSettings):
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    POSTGRES_DB: str

    timeout: int = 60  # in seconds
    statement_timeout: int = 55

    @property
    def full_url_async(self) -> str:
        url = URL.create(
            drivername=ASYNC_DRIVER_NAME,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
        )
        return url.render_as_string(hide_password=False)

    @property
    def full_url_sync(self) -> str:
        url = URL.create(
            drivername=SYNC_DRIVER_NAME,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            database=self.POSTGRES_DB,
        )
        return url.render_as_string(hide_password=False)


database_settings = DatabaseSettings()
