import uvicorn
from fastapi import FastAPI
from app.routers.api import api_router
from app.config.settings import HOST, LOCAL_HOST

app = FastAPI(
    title="Courier Service"
)

app.include_router(api_router)


# def run():
#     uvicorn.run("main:app", host=HOST, port=8000, reload=True)
#
#
# if __name__ == '__main__':
#     run()
