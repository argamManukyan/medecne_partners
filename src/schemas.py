from typing import Generic, Sequence
from src.utils import Model
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class BaseSchema(BaseModel):
    id: int | None = None


class PartnerCreateSchema(BaseModel):
    name: str
    email: EmailStr
    phone_number: str | None = None
    logo: str | None = None


class EmployeeCreateSchema(BaseModel):
    full_name: str
    email: EmailStr
    user_id: int
    partner_id: int


class EmployeeResponseSchema(BaseSchema, EmployeeCreateSchema):
    pass


class PartnerResponseSchema(BaseSchema, PartnerCreateSchema):
    model_config = ConfigDict(from_attributes=True)
    employee: list[EmployeeResponseSchema] = Field(default_factory=list)


class PaginationSchema(BaseSchema):
    offset: int = Field(gte=0)
    limit: int = Field(gte=4)


class PaginatedResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    total: int = 0
    data: Sequence[Model] = Field(default_factory=list)
