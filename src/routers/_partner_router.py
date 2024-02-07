from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.db_initialization import get_session
from src.dependencies import validate_request
from src.schemas import PartnerCreateSchema
from src.services import partner_service

partner_router = APIRouter()


@partner_router.post("/add-partner", dependencies=[Depends(validate_request)])
async def create_partner(
    session: AsyncSession = Depends(get_session), data: PartnerCreateSchema = Body(...)
):

    return await partner_service.create(session=session, data=data)
