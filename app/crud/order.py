from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.sql.base import ExecutableOption

from app.models import models


class CRUDOrder:
    """
    CRUD operation on order with session
    """
    async def get_by_sid(
            self,
            sid: UUID,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.Order).options(custom_options).where(models.Order.sid == sid)
        else:
            query = select(models.Order).where(models.Order.sid == sid)
        result: Result = await session.execute(query)
        return result.scalars().first()

    async def get_all(
            self,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.Order).options(custom_options)
        else:
            query = select(models.Order)
        result: Result = await session.execute(query)
        return result.scalars().all()


    async def create_or_update(
            self,
            order_obj: models.Order,
            session: AsyncSession,
            with_commit: bool = True
    ) -> models.Order:

        try:
            session.add(order_obj)
            if with_commit:
                await session.commit()
                await session.refresh(order_obj)
            else:
                await session.flush()
            return order_obj
        except:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Ошибка создания или обновления заказа")


order = CRUDOrder()
