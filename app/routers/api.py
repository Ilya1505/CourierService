from .courier import courier
from .order import order
from fastapi import APIRouter


api_router = APIRouter()

api_router.include_router(courier.router, tags=["Courier"], prefix='/courier')
api_router.include_router(order.router, tags=["Order"], prefix='/order')
