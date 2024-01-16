from typing import Annotated
from uuid import UUID
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.config.database import get_async_session
from app import crud, models, schemas
from sqlalchemy.orm import selectinload


router = APIRouter()


@router.post(path="/", response_model=schemas.Order)
async def create_order(
        order_new: Annotated[schemas.OrderCreate, Depends()],
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Order:
    """
    Method for creating an order in the system
    :param order_new: schemas.OrderCreate
    :param session: session with db
    :return: order object
    """
    couriers = await crud.courier.get_multi(district_name=order_new.district, session=session)

    for courier in couriers:
        flag = True
        for order in courier.orders:
            if order.status == '1':
                flag = False
        if flag:
            for district in courier.districts:
                print(district.name)
                print(order_new.name)
                if district.name == order_new.district:
                    order_obj = models.Order(
                            name=order_new.name,
                            courier_sid=courier.sid,
                            district_sid=district.sid
                        )
                    return await crud.order.create_or_update(order_obj=order_obj, session=session)
            break

    raise HTTPException(status_code=400, detail="Нет подходящего курьера")


@router.get(path="/{sid}", response_model=schemas.OrderSID)
async def get_order_by_sid(
        sid: UUID,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.OrderSID:
    """
    Method for receiving order information by its ID
    :param sid: UUID
    :param session: session with db
    :return: order object
    """
    order = await crud.order.get_by_sid(sid=sid, session=session)
    if not order:
        raise HTTPException(status_code=400, detail="Неккоректный sid заказа")
    return order


@router.post(path="/{sid}", response_model=schemas.Order)
async def finish_order(
        sid: UUID,
        session: AsyncSession = Depends(get_async_session)
) -> schemas.Order:
    """
    Order completion method
    :param sid: UUID
    :param session: session with db
    :return: order object
    """
    order = await crud.order.get_by_sid(sid=sid, session=session, custom_options=selectinload(models.Order.courier))
    if not order:
        raise HTTPException(status_code=400, detail="Неккоректный sid заказа")
    elif order.status == '2':
        raise HTTPException(status_code=400, detail="Заказ завершен")

    if order.courier.number_completed == 0:
        order.courier.avg_order_complete_time = datetime.now() - order.registration_at
    else:
        total_time = order.courier.avg_order_complete_time * order.courier.number_completed
        order.courier.avg_order_complete_time \
            = (total_time + (datetime.now() - order.registration_at)) / (order.courier.number_completed + 1)

    order.courier.avg_day_orders \
        = (order.courier.number_completed + 1) / ((datetime.now() - order.registration_at).days + 1)

    order.courier.number_completed += 1
    order.status = '2'

    return await crud.order.create_or_update(order_obj=order, session=session)
