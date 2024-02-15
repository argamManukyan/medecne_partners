from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import partner_repository
from src.schemas import (
    PartnerCreateSchema,
    PaginationSchema,
    PaginatedResponseSchema,
    PartnerResponseSchema,
)
from src.utils import validate_unique_args


class PartnerService:

    repository = partner_repository

    @classmethod
    @validate_unique_args(model=repository.model, filter_func=repository.filter_by_args)
    async def create(cls, session: AsyncSession, data: PartnerCreateSchema):
        obj = await cls.repository.create(session=session, **data.model_dump())
        return obj

    @classmethod
    async def list_partners(
        cls, session: AsyncSession, pagination: PaginationSchema
    ) -> PaginatedResponseSchema:
        total = await cls.repository.get_total(session=session)

        data = await cls.repository.filter_by_args(
            session=session, offset=pagination.offset, limit=pagination.limit
        )

        return PaginatedResponseSchema(total=total, data=data)

    @classmethod
    async def get(cls, partner_id: int, session: AsyncSession) -> PartnerResponseSchema:
        return await cls.repository.get(session=session, obj_id=partner_id)
