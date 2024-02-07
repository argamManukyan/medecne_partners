from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories import partner_repository
from src.schemas import PartnerCreateSchema


class PartnerService:

    repository = partner_repository

    @classmethod
    async def create(cls, session: AsyncSession, data: PartnerCreateSchema):
        return await cls.repository.create(session=session, **data.model_dump())
