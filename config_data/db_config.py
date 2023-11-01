import os

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.engine import URL


def get_async_engine(url: str) -> AsyncEngine:
    return create_async_engine(url=url, echo=True, pool_pre_ping=True)


def get_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker:
    return async_sessionmaker(bind=engine, class_=AsyncSession)


POSTGRES_URL = (f'postgresql+asyncpg://'
                f'{os.getenv("POSTGRES_USER")}:'
                f'{os.getenv("POSTGRES_PASSWORD")}@'
                f'{os.getenv("POSTGRES_HOST")}:'
                f'{os.getenv("POSTGRES_PORT")}/'
                f'{os.getenv("POSTGRES_DB")}')
