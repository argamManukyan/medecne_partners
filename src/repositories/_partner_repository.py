from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from src.exceptions import ObjectDoesNotExists
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
    async def create(cls, session: AsyncSession, **kwargs) -> response_schema:
        obj: cls.response_schema = await super().create(session=session, **kwargs)
        return await cls.get(session=session, obj_id=obj.id)

    @classmethod
    async def filter_by_args(
        cls, session: AsyncSession, offset: int = 0, limit: int = 10, **kwargs
    ) -> Sequence[PartnerResponseSchema]:
        """Returns a filtered data instance using the given attributes"""

        stmt = await super().filter_by_args(
            session=session, offset=offset, limit=limit, **kwargs
        )
        result = await session.scalars(stmt)
        return [cls.response_schema.from_orm(partner) for partner in result.all()]

    @classmethod
    @join_with(join_tables, model)
    async def get(
        cls, session: AsyncSession, obj_id: int, options_l: list = None
    ) -> response_schema:
        """Returns an instance of model"""

        stmt = await super().get(session=session, obj_id=obj_id)
        stmt = stmt.options(*options_l)
        result = await session.scalars(stmt)
        res = result.one_or_none()
        if res:
            return cls.response_schema.from_orm(res)
        raise ObjectDoesNotExists
