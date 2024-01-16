from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class OrderBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderSID(BaseModel):
    sid: UUID
    courier_sid: UUID


class OrderCreate(OrderBase):
    name: str
    district: str


class Order(OrderBase):
    sid: UUID
    name: str
    status: int
    courier_sid: UUID
