from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepositoryMixin:
    """Generic repository mixin"""

    model = None
    response_schema = None
    join_tables = []

    @classmethod
    async def get(cls, session: AsyncSession, obj_id: int):
        stmt = select(cls.model).filter_by(id=obj_id)
        return stmt

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        instance = cls.model(**kwargs)
        session.add(instance)
        await session.commit()
        return await cls.get(session=session, obj_id=instance.id)
