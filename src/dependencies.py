from fastapi import Header
from src.core.configs import settings
from src.exceptions import PermissionDenied
from src.schemas import PaginationSchema


SECRET_KEY = settings.app_settings.SECRET_KEY


def validate_request(secret_key: str = Header(...)) -> bool:
    """Verifies is the request received from API Gateway"""
    if secret_key != SECRET_KEY:
        raise PermissionDenied
    return True


def pagination(limit: int = 10, offset: int = 0):
    return PaginationSchema(limit=limit, offset=offset)
