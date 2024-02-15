from functools import wraps
from fastapi import status
from sqlalchemy import inspect
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.relationships import RelationshipProperty
from sqlalchemy import Column
from typing import Callable, TypeVar, Awaitable, Any

from src.exceptions import GenericException

Model = TypeVar("Model")


def _get_related_columns(table: Model) -> list[RelationshipProperty]:
    """Returns all kind of relations of the table"""

    inspection = inspect(table)
    return list(inspection.relationships)


def _get_local_columns(table: Model) -> list[Column]:
    inspection = inspect(table)
    return list(inspection.columns)


def join_with(join_models: list[Model], main_model: Model):
    """Returns all selected joins for the particular request"""

    def inner(func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            # taking out of related columns
            related_columns = _get_related_columns(main_model)

            # filtering and catching all joining columns
            filtered_relation_columns = list(
                filter(lambda col: col.mapper.entity in join_models, related_columns)
            )

            options_list = (
                list()
            )  # Grouping all kind of selections such as selectinload or joinedload

            for rel_column in filtered_relation_columns:
                if rel_column.uselist:
                    options_list.append(
                        selectinload(getattr(main_model, str(rel_column.key)))
                    )

            return await func(options_l=options_list, *args, **kwargs)

        return wrapper

    return inner


def validate_unique_args(
    model: Model, filter_func: Callable[[Any, Any], Awaitable[Any]]
):
    def inner(func: Callable):

        @wraps(func)
        async def wrapper(*args, **kwargs):

            unique_columns = [i.name for i in _get_local_columns(model) if i.unique]
            session = kwargs.get("session")
            data = kwargs.get("data")

            for col in unique_columns:
                filter_d = {col: getattr(data, col)}

                res = await filter_func(session, **filter_d)  # check existing

                if res:
                    message = f"The {model.__tablename__.title()} with given {col} already exists."

                    raise GenericException(
                        detail=message,
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    )

            return await func(*args, **kwargs)

        return wrapper

    return inner
