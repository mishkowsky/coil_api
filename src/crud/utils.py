from typing import Optional, TypeVar
from sqlalchemy import and_
from sqlalchemy.sql.elements import ColumnElement
from src.schemas.coil import Range


def combine_conditions_with_and(
        condition1: Optional[ColumnElement[bool]],
        condition2: ColumnElement[bool]) -> ColumnElement[bool]:
    if condition1 is None:
        condition1 = condition2
    else:
        condition1 = and_(condition1, condition2)
    return condition1


def construct_range_condition(input_range: Range, column: ColumnElement) -> ColumnElement[bool]:
    return and_(input_range.start <= column, column <= input_range.end)


T = TypeVar('T')


def add_range_condition(condition: Optional[ColumnElement[bool]],
                        input_range: Range[T],
                        column_attribute: T) -> Optional[ColumnElement[bool]]:
    if input_range is not None:
        id_condition = construct_range_condition(input_range, column_attribute)
        condition = combine_conditions_with_and(condition, id_condition)
    return condition
