from sqlalchemy.ext.asyncio import AsyncSession
from src.models import Partner, Employee
from src.repositories.base import BaseRepositoryMixin
from src.schemas import PartnerResponseSchema
from src.utils import join_with


class PartnerRepository(BaseRepositoryMixin):
    """Repository pattern for Partner's"""

    model = Partner
    response_schema = PartnerResponseSchema
    join_tables = [Employee]

    @classmethod
    async def create(cls, session: AsyncSession, **kwargs):
        return await super().create(session=session, **kwargs)

    @classmethod
    @join_with(join_tables, model)
    async def get(cls, session: AsyncSession, obj_id: int, options_l: list = None):
        obj = await super().get(session=session, obj_id=obj_id)
        stmt = obj.options(*options_l)
        t = await session.scalars(stmt)
        return t.one_or_none()

    # @classmethod
    # async def create(cls, session: AsyncSession, **kwargs) -> response_schema:
    #     instance = cls.model(**kwargs)
    #     session.add(instance)
    #     await session.commit()
    #     return cls.response_schema.model_validate(instance)
