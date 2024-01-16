from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime, timedelta


class CourierBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    name: str


class CourierCreate(CourierBase):
    districts: list[str]


class Courier(CourierBase):
    sid: UUID
    registration_at: datetime
    number_completed: int
    active_order: dict | None = None
    avg_order_complete_time: timedelta | None
    avg_day_orders: int | None


class CourierAll(CourierBase):
    sid: UUID


class CourierXDistrictBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    courier_sid: UUID
    district_sid: UUID


class District(BaseModel):
    sid: UUID
    name: str

