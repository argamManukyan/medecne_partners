from pydantic import BaseModel, EmailStr, Field


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
    employee: list[EmployeeResponseSchema] = Field(default_factory=list)
