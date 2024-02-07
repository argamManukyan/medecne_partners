from fastapi import HTTPException, status
from src.messages import PERMISSION_DENIED

PermissionDenied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail=PERMISSION_DENIED
)
