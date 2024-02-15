from typing import Any
from fastapi import HTTPException, status
from src.messages import error_messages

PermissionDenied = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN, detail=error_messages.PERMISSION_DENIED
)

ObjectDoesNotExists = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail=error_messages.OBJECT_DOES_NOT_EXISTS
)


class GenericException(HTTPException):

    def __init__(
        self,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        detail: Any = error_messages.SOMETHING_WENT_WRONG,
        *args,
        **kwargs
    ) -> None:
        super().__init__(status_code, detail, *args, **kwargs)
