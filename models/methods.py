from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy import select

from models.models import User


async def get_user(user_id: int, session: async_sessionmaker) -> User:
    async with session() as session:
        async with session.begin():
            user = await session.execute(select(User).where(User.id == user_id))
            return user.first()


async def is_user_exist(user_id: int, session: async_sessionmaker):
    async with session() as session:
        sql_res = await session.execute(select(User).where(User.id == user_id))
        sql_res = sql_res.one_or_none()
        return bool(sql_res)


async def create_user(user_id: int, session: async_sessionmaker):
    async with session() as session:
        user = User(id=user_id)
        session.add(user)
        await session.commit()
