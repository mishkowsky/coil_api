from datetime import datetime, timedelta
from typing import Generic, Optional, TypeVar, Annotated
from pydantic import BaseModel, model_validator, Field


class CoilBase(BaseModel):
    length: Annotated[int, Field(strict=True, gt=0)]
    weight: Annotated[int, Field(strict=True, gt=0)]


class CoilCreate(CoilBase):
    pass


class CoilToUpdate(BaseModel):
    id: Annotated[int, Field(strict=True, gt=0)]


class CoilUpdate(BaseModel):
    deleted_at: datetime


class CoilInDBBase(CoilBase):
    id: Optional[int] = None
    created_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class Coil(CoilInDBBase, BaseModel):
    pass


T = TypeVar("T", int, datetime)


class Range(BaseModel, Generic[T]):
    start: T
    end: T

    @model_validator(mode='after')
    def check_bounds(self):
        if self.start > self.end:
            raise ValueError('start value must not be more than end value')
        return self


class GetCoilRequestBody(BaseModel):
    id_range: Optional[Range[Annotated[int, Field(gt=0)]]] = None
    length_range: Optional[Range[Annotated[int, Field(gt=0)]]] = None
    weight_range: Optional[Range[Annotated[int, Field(gt=0)]]] = None
    created_at_range: Optional[Range[datetime]] = None
    deleted_at_range: Optional[Range[datetime]] = None

    @model_validator(mode='after')
    def check_at_least_one_range_is_present(self):
        if not self.id_range and not self.length_range and not self.weight_range and \
                not self.created_at_range and not self.deleted_at_range:
            raise ValueError('either one of range is required')
        return self


class StatResponseBody(BaseModel):
    added_coils_count: Optional[int] = 0
    deleted_coils_count: Optional[int] = 0
    avg_length: Optional[float] = 0
    avg_weight: Optional[float] = 0
    max_length: Optional[int] = None
    min_length: Optional[int] = None
    max_weight: Optional[int] = None
    min_weight: Optional[int] = None
    total_weight: Optional[int] = 0
    min_period: Optional[timedelta] = None
    max_period: Optional[timedelta] = None
