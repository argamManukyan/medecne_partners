from sqlalchemy import String, URL, UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.db_initialization import AbstractModel


class Employee(AbstractModel):
    __tablename__ = "employee"
    __table_args__ = (
        UniqueConstraint(
            "partner_id", "user_id", "id", name="employee_unique_constraint"
        ),
    )
    full_name: Mapped[str]
    email: Mapped[str]
    user_id: Mapped[int]
    partner: Mapped["Partner"] = relationship(
        "Partner", back_populates="employees", cascade="all, delete-orphan"
    )
    partner_id: Mapped[int] = mapped_column(Integer, ForeignKey("partner.id"))


class Partner(AbstractModel):
    __tablename__ = "partner"
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50))
    logo: Mapped[URL] = mapped_column(String)
    employee: Mapped[list[Employee]] = relationship(
        "Employee",
        back_populates="user",
    )
