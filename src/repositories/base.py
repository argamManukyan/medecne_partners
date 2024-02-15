from sqlalchemy import select, func
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
    async def filter_by_args(
        cls, session: AsyncSession, offset: int = 0, limit: int = 10, **kwargs
    ):
        """Returns a sequence of filtered objects by using given kwargs"""
        return select(cls.model).filter_by(**kwargs).offset(offset).limit(limit)

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs) -> response_schema:
        instance = cls.model(**kwargs)
        session.add(instance)
        await session.commit()
        return cls.response_schema.from_orm(instance)

    @classmethod
    async def get_total(cls, session: AsyncSession) -> int:
        res = await session.execute(select(func.count(cls.model.id)))
        return res.scalar_one()
