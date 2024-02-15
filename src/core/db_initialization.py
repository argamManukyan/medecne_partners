import datetime
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import MetaData, text, DateTime
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from src.exceptions import GenericException
from src.core.configs import settings


engine = create_async_engine(settings.db_settings.db_url)

async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session():
    async with async_session() as session:
        try:
            yield session
        except IntegrityError as e:
            await session.rollback()
            raise GenericException(detail=f"{e}", status_code=e.status_code)


meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_`%(constraint_name)s`",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)

Base = declarative_base(metadata=meta)


class AbstractModel(Base):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=False,
        default=datetime.datetime.utcnow,
        server_default=text("CURRENT_TIMESTAMP"),
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=False),
        nullable=True,
        onupdate=text("CURRENT_TIMESTAMP"),
    )

    def __repr__(self):
        return f"<{self.__class__.__name__}: {self.id}>"
