from sqlalchemy import String, UniqueConstraint, Integer, ForeignKey
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
    partner: Mapped["Partner"] = relationship("Partner", back_populates="employees")
    partner_id: Mapped[int] = mapped_column(Integer, ForeignKey("partner.id"))


class Partner(AbstractModel):
    __tablename__ = "partner"
    name: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(50))
    phone_number: Mapped[str] = mapped_column(String(50), nullable=True)
    logo: Mapped[str] = mapped_column(String, nullable=True)
    employees: Mapped[list[Employee]] = relationship(
        "Employee", back_populates="partner", cascade="all, delete-orphan"
    )
