from fastapi import APIRouter, Depends
from src.dependencies import validate_request


employee_router = APIRouter(
    prefix="/employee", dependencies=[Depends(validate_request)]
)
