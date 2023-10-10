from datetime import datetime
from typing import List, Type
from sqlalchemy import and_, func, or_, cast, Float, not_
from sqlalchemy.orm import Session
from src.crud.base import CRUDBase
from src.crud.utils import add_range_condition
from src.database.model import Coil
from src.schemas.coil import CoilCreate, CoilUpdate, GetCoilRequestBody, StatResponseBody


class CRUDCoil(CRUDBase[Coil, CoilCreate, CoilUpdate]):

    def get_coils_by_ranges(self, db: Session, request: GetCoilRequestBody) -> List[Type[Coil]]:
        condition = add_range_condition(None, request.id_range, self.model.id)
        condition = add_range_condition(condition, request.weight_range, self.model.weight)
        condition = add_range_condition(condition, request.length_range, self.model.length)
        condition = add_range_condition(condition, request.created_at_range, self.model.created_at)
        condition = add_range_condition(condition, request.deleted_at_range, self.model.deleted_at)
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
