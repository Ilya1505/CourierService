from uuid import UUID
from typing import Annotated, Sequence
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app import crud, models, schemas
from app.config.database import get_async_session

router = APIRouter()


@router.post(path="/create_district", response_model=schemas.District)
async def create_district(
        district_name: str,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.District:
    """
    District creation method
    :param district_name: str
    :param session: session with db
    :return: district object
    """
    district_obj = models.District(name=district_name)
    return await crud.district.create(district_obj=district_obj, session=session)


@router.get(path="/get_districts", response_model=Sequence[schemas.District])
async def get_districts(
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[schemas.District]:
    """
    Method for getting a list of districts
    :param session: session with db
    :return: sequence of district object
    """
    return await crud.district.get_all(session=session)


@router.post(path="/", response_model=schemas.Courier)
async def create_courier(
        courier_in: Annotated[schemas.CourierCreate, Depends()],
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Courier:
    """
    Method of registering a courier in the system
    :param courier_in: schemas.CourierCreate
    :param session: session with db
    :return: courier object
    """

    # Получение списка всех районов системы
    all_district = await crud.district.get_all(session=session)

    district_name = list()
    for district in all_district:
        district_name.append(district.name)

    # Проверка что данные от пользователя корректны
    for district_new in courier_in.districts:
        if district_new not in district_name:
            raise HTTPException(status_code=400, detail="Неккоректное имя района")

    # Создание модели курьера
    courier_obj = models.Courier(name=courier_in.name)
    await crud.courier.create(courier_obj=courier_obj, session=session, with_commit=False)

    # Создание моделей courier_x_district
    for district in all_district:
        if district.name in courier_in.districts:
            courier_x_district_obj = models.CourierXDistrict(
                courier_sid=courier_obj.sid,
                district_sid=district.sid
            )
            await crud.courier_x_district.create(courier_x_district_obj=courier_x_district_obj, session=session)
    return courier_obj


@router.get(path="/", response_model=Sequence[schemas.CourierAll])
async def get_couriers(
        session: AsyncSession = Depends(get_async_session)
) -> Sequence[schemas.CourierAll]:
    """
    Method for getting a list of all couriers
    :param session: session with db
    :return: courier object
    """
    return await crud.courier.get_all(session=session)


@router.get(path="/{sid}", response_model=dict)
async def get_courier_by_sid(
        sid: UUID,
        session: AsyncSession = Depends(get_async_session)
) -> dict:
    """
    Method of getting a courier by his ID
    :param sid: UUID
    :param session: session with db
    :return: dict of courier object
    """
    # Получение курьера по sid
    courier = await crud.courier.get_by_sid(
        sid=sid,
        session=session,
        custom_options=selectinload(models.Courier.orders)
    )

    if not courier:
        raise HTTPException(status_code=400, detail="Неккоректный sid курьера")

    active_order = None
    for order in courier.orders:
        if order.status == '1':
            active_order = {"order_id": order.sid, "order_name": order.name}
            break

    courier_dict = {
        "sid": courier.sid,
        "name": courier.name,
        "registration_at": courier.registration_at,
        "number_completed": courier.number_completed,
        "active_order": active_order,
        "avg_order_complete_time": courier.avg_order_complete_time,
        "avg_day_orders": courier.avg_day_orders
    }
    return courier_dict


