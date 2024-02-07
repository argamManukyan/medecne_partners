from sqlalchemy import inspect
from sqlalchemy.orm import selectinload
from sqlalchemy.orm.relationships import RelationshipProperty
from typing import Callable, TypeVar
from functools import wraps


Model = TypeVar("Model")


def _get_related_columns(table: Model) -> list[RelationshipProperty]:
    """Returns all kind of relations of the table"""

    inspection = inspect(table)
    return list(inspection.relationships)


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
                []
            )  # Grouping all kind of selections such as selectinload or joinedload

            for rel_column in filtered_relation_columns:
                if rel_column.uselist:
                    options_list.append(
                        selectinload(getattr(main_model, str(rel_column.key)))
                    )

            return await func(options_l=options_list, *args, **kwargs)

        return wrapper

    return inner
