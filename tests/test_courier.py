from app import models
from conftest import client, async_session_maker

async def test_init_districts():
    async with async_session_maker() as session:
        new_district = models.District(name="test_district1")
        session.add(new_district)
        await session.commit()


async def test_create_courier():
    responce = client.post("/courier/", params={"name": "test_courier1"}, json=["test_district1"])

    assert responce.status_code == 200
    assert responce.json()["name"] == "test_courier1"

def test_get_couriers():
    responce = client.get("/courier/")

    assert responce.status_code == 200
    assert len(responce.json()) > 0, "Таблица курьеров пуста"