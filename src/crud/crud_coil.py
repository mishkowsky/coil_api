from datetime import datetime
from typing import List, Type
from sqlalchemy import and_, func, or_, cast, Float, not_
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.crud.utils import combine_conditions_with_and
from src.database.model import Coil
from src.schemas.coil import CoilCreate, CoilUpdate, GetCoilRequestBody, StatResponseBody


class CRUDCoil(CRUDBase[Coil, CoilCreate, CoilUpdate]):

    def get_by_period(self, db: Session, start_time: datetime, end_time: datetime) -> List[Type[Coil]]:
        return db.query(self.model).filter(self.model.created_at < end_time or self.model.deleted_at > start_time).all()

    def get_coils_by_ranges(self, db: Session, request: GetCoilRequestBody) -> List[Type[Coil]]:

        condition = None

        if request.id_range is not None:
            id_condition = and_(
                request.id_range.start <= self.model.id,
                self.model.id <= request.id_range.end
            )
            condition = combine_conditions_with_and(condition, id_condition)
        if request.weight_range is not None:
            weight_condition = and_(
                request.weight_range.start <= self.model.weight,
                self.model.weight <= request.weight_range.end
            )
            condition = combine_conditions_with_and(condition, weight_condition)
        if request.length_range is not None:
            length_condition = and_(
                request.length_range.start <= self.model.length,
                self.model.length <= request.length_range.end
            )
            condition = combine_conditions_with_and(condition, length_condition)
        if request.created_at_range is not None:
            created_at_condition = and_(
                request.created_at_range.start <= self.model.created_at,
                self.model.created_at <= request.created_at_range.end
            )
            condition = combine_conditions_with_and(condition, created_at_condition)
        if request.deleted_at_range is not None:
            deleted_at_condition = and_(
                request.deleted_at_range.start <= self.model.deleted_at,
                self.model.deleted_at <= request.deleted_at_range.end
            )
            condition = combine_conditions_with_and(condition, deleted_at_condition)
        result = db.query(self.model).filter(condition).all()
        return result

    def get_stats(self, db: Session, start_date: datetime, end_date: datetime) -> StatResponseBody:
        # ~((delete < start & delete != None) | (create > end))
        filter_condition = not_(or_(self.model.created_at > end_date,
                                    and_(self.model.deleted_at < start_date, self.model.deleted_at != None)))

        res = db.query(
            func.max(self.model.weight).label('max_weight'),
            func.min(self.model.weight).label('min_weight'),
            cast(func.avg(self.model.weight).label('avg_weight'), Float),
            func.sum(self.model.weight).label('total_weight'),

            func.max(self.model.length).label('max_length'),
            func.min(self.model.length).label('min_length'),
            cast(func.avg(self.model.length).label('avg_length'), Float),

            func.max(self.model.deleted_at - self.model.created_at).
            filter(self.model.deleted_at is not None).label('max_period'),
            func.min(self.model.deleted_at - self.model.created_at).
            filter(self.model.deleted_at is not None).label('min_period'),

            func.count(self.model.id).filter(self.model.created_at >= start_date).label('added_coils_count'),
            func.count(self.model.id).filter(self.model.deleted_at <= end_date).label('deleted_coils_count'),
        ).filter(filter_condition).one_or_none()
        return StatResponseBody(
            max_weight=res[0] or None,
            min_weight=res[1] or None,
            avg_weight=res[2] or 0,
            total_weight=res[3] or 0,
            max_length=res[4] or None,
            min_length=res[5] or None,
            avg_length=res[6] or 0,
            max_period=res[7] or None,
            min_period=res[8] or None,
            added_coils_count=res[9] or 0,
            deleted_coils_count=res[10] or 0
        )


coil = CRUDCoil(Coil)
