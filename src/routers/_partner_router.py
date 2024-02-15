from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_initialization import get_session
from src.dependencies import validate_request, pagination
from src.schemas import (
    PartnerCreateSchema,
    PartnerResponseSchema,
    PaginatedResponseSchema,
    PaginationSchema,
)
from src.services import partner_service

partner_router = APIRouter(dependencies=[Depends(validate_request)])


@partner_router.post(
    "/partner",
    response_model=PartnerResponseSchema,
)
async def create_partner(
    session: AsyncSession = Depends(get_session), data: PartnerCreateSchema = Body(...)
):

    return await partner_service.create(session=session, data=data)


@partner_router.get(
    "/partner",
    response_model=PaginatedResponseSchema,
)
async def partners_list(
    session: AsyncSession = Depends(get_session),
    page_data: PaginationSchema = Depends(pagination),
):
    return await partner_service.list_partners(session=session, pagination=page_data)


@partner_router.get(
    "/partner/{partner_id}",
    response_model=PartnerResponseSchema,
)
async def get_partner(
    partner_id: int,
    session: AsyncSession = Depends(get_session),
):

    return await partner_service.get(session=session, partner_id=partner_id)
