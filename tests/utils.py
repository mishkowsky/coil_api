from datetime import datetime
from functools import partial
from typing import List
from src.database.model import Coil
from src.schemas.coil import StatResponseBody


def is_coil_matches_period(test_coil: Coil, start_date: datetime, end_date: datetime) -> bool:
    return test_coil.created_at <= end_date and (test_coil.deleted_at is None or test_coil.deleted_at >= start_date)


def count_stats_for_test_data(test_coils: List[Coil], start_date: datetime, end_date: datetime) -> StatResponseBody:
    stats = StatResponseBody()

    coils_in_period = list(
        filter(partial(is_coil_matches_period, start_date=start_date, end_date=end_date), test_coils))

    stats.min_length = min(test_coil.length for test_coil in coils_in_period)
    stats.max_length = max(test_coil.length for test_coil in coils_in_period)

    stats.min_weight = min(test_coil.weight for test_coil in coils_in_period)
    stats.max_weight = max(test_coil.weight for test_coil in coils_in_period)

    stats.total_weight = sum(test_coil.weight for test_coil in coils_in_period)
    stats.avg_weight = stats.total_weight / len(coils_in_period)

    stats.avg_length = sum(test_coil.length for test_coil in coils_in_period) / len(coils_in_period)

    deleted_test_coils = list(filter(lambda test_coil: test_coil.deleted_at is not None, coils_in_period))
    stats.max_period = max(test_coil.deleted_at - test_coil.created_at for test_coil in deleted_test_coils)
    stats.min_period = min(test_coil.deleted_at - test_coil.created_at for test_coil in deleted_test_coils)

    stats.deleted_coils_count = len(list(filter(
        lambda test_coil: test_coil.deleted_at is not None and test_coil.deleted_at < end_date, coils_in_period
    )))
    stats.added_coils_count = len(list(filter(lambda test_coil: test_coil.created_at > start_date, coils_in_period)))

    return stats
