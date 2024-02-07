from src.core.configs import settings
from src.exceptions import PermissionDenied

SECRET_KEY = settings.app_settings.SECRET_KEY


def validate_request(secret_key: str) -> bool:
    """Verifies is the request received from API Gateway"""

    if secret_key != SECRET_KEY:
        raise PermissionDenied
    return True
