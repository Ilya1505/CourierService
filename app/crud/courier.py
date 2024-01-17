from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.models import models


class CRUDCourier:
    """
    CRUD operation on courier with session
    """
    async def get_by_sid(
            self,
            sid: UUID,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.Courier).options(custom_options).where(models.Courier.sid == sid)
        else:
            query = select(models.Courier).where(models.Courier.sid == sid)
        result: Result = await session.execute(query)
        return result.scalars().first()

    async def get_all(
            self,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.Courier).options(custom_options)
        else:
            query = select(models.Courier)
        result: Result = await session.execute(query)
        return result.scalars().all()

    async def get_multi(
            self,
            district_name: str,
            session: AsyncSession,
    ):
        # Зпрос на получение всех курьеров, из определенного района
        query = select(models.Courier).options(selectinload(models.Courier.orders),
                                               selectinload(models.Courier.districts)) \
            .join(models.CourierXDistrict, models.CourierXDistrict.courier_sid == models.Courier.sid) \
            .join(models.District, models.District.sid == models.CourierXDistrict.district_sid) \
            .where(models.District.name == district_name)
        result: Result = await session.execute(query)
        return result.scalars().all()

    async def create(
            self,
            courier_obj: models.Courier,
            session: AsyncSession,
            with_commit: bool = True
    ) -> models.Courier:

        try:
            session.add(courier_obj)
            if with_commit:
                await session.commit()
                await session.refresh(courier_obj)
            else:
                await session.flush()
            return courier_obj
        except:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Ошибка создания курьера")


class CRUDCourierXDistrict:

    async def create(
            self,
            courier_x_district_obj: models.CourierXDistrict,
            session: AsyncSession,
            with_commit: bool = True
    ) -> models.CourierXDistrict:

        try:
            session.add(courier_x_district_obj)
            if with_commit:
                await session.commit()
                await session.refresh(courier_x_district_obj)
            else:
                await session.flush()
            return courier_x_district_obj
        except:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Ошибка создания courier_x_district")


courier = CRUDCourier()
courier_x_district = CRUDCourierXDistrict()
