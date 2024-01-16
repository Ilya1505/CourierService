from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.base import ExecutableOption

from app.models import models


class CRUDDistrict:
    """
    CRUD operation on district with session
    """
    async def get_by_sid(
            self,
            sid: UUID,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.District).options(custom_options).where(models.District.sid == sid)
        else:
            query = select(models.District).where(models.District.sid == sid)
        result: Result = await session.execute(query)
        return result.scalars().first()

    async def get_all(
            self,
            session: AsyncSession,
            custom_options: ExecutableOption = None

    ):
        if isinstance(custom_options, ExecutableOption):
            query = select(models.District).options(custom_options)
        else:
            query = select(models.District)
        result: Result = await session.execute(query)
        return result.scalars().all()

    async def create(
            self,
            district_obj: models.District,
            session: AsyncSession,
            with_commit: bool = True
    ) -> models.District:

        try:
            session.add(district_obj)
            if with_commit:
                await session.commit()
                await session.refresh(district_obj)
            else:
                await session.flush()
            return district_obj
        except:
            await session.rollback()
            raise HTTPException(status_code=400, detail="Ошибка создания района")


district = CRUDDistrict()
