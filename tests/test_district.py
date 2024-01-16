from sqlalchemy import select, Result
from conftest import client, async_session_maker
from app import models


async def test_create_district():
    async with async_session_maker() as session:
        new_district = models.District(name="test_district")
        session.add(new_district)
        await session.commit()

        query = select(models.District).where(models.District.name == "test_district")
        result: Result = await session.execute(query)
        get_district = result.scalars().first()
        assert new_district.name == get_district.name, "Район не добавился"

def test_get_districts():
    responce = client.get("/courier/get_districts")

    assert responce.status_code == 200
    assert len(responce.json()) > 0, "Таблица районов пуста"
