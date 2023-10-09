from sqlalchemy import and_


def combine_conditions_with_and(condition1, condition2):
    if condition1 is None:
        condition1 = condition2
    else:
        condition1 = and_(condition1, condition2)
    return condition1
