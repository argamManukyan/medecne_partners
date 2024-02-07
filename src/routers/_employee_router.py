from fastapi import APIRouter
from src.dependencies import validate_request


employee_router = APIRouter(prefix="/employee", dependencies=[validate_request])
