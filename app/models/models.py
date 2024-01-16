from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime, timedelta
from app.config.database import Base

SCHEMA = 'public'


class Courier(Base):
    """
    Table with Courier data
    """

    __tablename__ = "courier"
    __table_args__ = {
        'schema': SCHEMA,
        'comment': 'Table with all Courier'
    }

    sid: Mapped[UUID] = mapped_column(
        unique=True,
        primary_key=True,
        index=True,
        default=lambda: uuid4().hex
    )
    name: Mapped[str] = mapped_column(index=True, comment='name of courier')
    number_completed: Mapped[int] = mapped_column(default=0, comment='number of completed orders')
    registration_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.now().replace(microsecond=0),
        comment='time of registration'
    )
    avg_order_complete_time: Mapped[timedelta] = mapped_column(default=timedelta(), comment='average order complete time', nullable=True)
    avg_day_orders: Mapped[int] = mapped_column(default=0, comment='average number of completed orders per day', nullable=True)

    districts: Mapped[list["District"]] = relationship(secondary="public.courier_x_district", back_populates="couriers")
    orders: Mapped[list["Order"]] = relationship(back_populates="courier")

    def __init__(self, name, registration_at=None, number_completed=0):
        self.sid = uuid4().hex
        self.name = name
        self.number_completed = number_completed
        self.registration_at = registration_at


class District(Base):
    """
    Table with District data
    """

    __tablename__ = "district"
    __table_args__ = {
        'schema': SCHEMA,
        'comment': 'Table with District data'
    }

    sid: Mapped[UUID] = mapped_column(
        unique=True,
        primary_key=True,
        index=True,
        default=lambda: uuid4().hex
    )
    name: Mapped[str] = mapped_column(index=True, comment='name of courier')

    couriers: Mapped[list["Courier"]] = relationship(secondary="public.courier_x_district", back_populates="districts")
    orders: Mapped[list["Order"]] = relationship(back_populates="district")

    def __init__(self, name):
        self.sid = uuid4().hex
        self.name = name


class CourierXDistrict(Base):

    __tablename__ = "courier_x_district"
    __table_args__ = {
        'schema': SCHEMA,
        'comment': 'Table with districts for Courier'
    }

    courier_sid: Mapped[UUID] = mapped_column(ForeignKey("public.courier.sid"), primary_key=True)
    district_sid: Mapped[UUID] = mapped_column(ForeignKey("public.district.sid"), primary_key=True)

    def __init__(self, courier_sid, district_sid):
        self.courier_sid = courier_sid
        self.district_sid = district_sid


class Order(Base):
    """
    Table with Order data
    """

    __tablename__ = "order"
    __table_args__ = {
        'schema': SCHEMA,
        'comment': 'Table with orders data'
    }

    sid: Mapped[UUID] = mapped_column(
        unique=True,
        primary_key=True,
        index=True,
        default=lambda: uuid4().hex
    )
    name: Mapped[str] = mapped_column(index=True, comment='name of order')
    status: Mapped[str] = mapped_column(index=True, default='1', comment='status of order: 1 - in work, 2 - completed')
    registration_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.now().replace(microsecond=0),
        comment='time of registration'
    )
    courier_sid: Mapped[UUID] = mapped_column(ForeignKey("public.courier.sid"))
    district_sid: Mapped[UUID] = mapped_column(ForeignKey("public.district.sid"))

    courier: Mapped["Courier"] = relationship(back_populates="orders")
    district: Mapped["District"] = relationship(back_populates="orders")

    def __init__(self, name, courier_sid, district_sid):
        self.sid = uuid4().hex
        self.name = name
        self.status = '1'
        self.courier_sid = courier_sid
        self.district_sid = district_sid
