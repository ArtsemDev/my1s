from pathlib import Path
from typing import Union

from pydantic import PostgresDsn, MariaDBDsn, MySQLDsn
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from orjson import loads, dumps

__all__ = ["settings", "async_session_maker", "async_engine"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(frozen=True, case_sensitive=False)

    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    DATABASE_URL: Union[PostgresDsn, MariaDBDsn, MySQLDsn]


settings = Settings()
async_engine = create_async_engine(
    url=settings.DATABASE_URL.unicode_string(),
    json_serializer=dumps,
    json_deserializer=loads,
)
async_session_maker = async_sessionmaker(bind=async_engine, expire_on_commit=False)
