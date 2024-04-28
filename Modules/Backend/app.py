from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

from database import DBWorker
from routes import data_router
from utils import PredictModel


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.include_router(data_router, tags=['Работа с данными'])

    PredictModel.load_model()

    await DBWorker.start_database()

    from mqtt import fast_mqtt
    await fast_mqtt.mqtt_startup()

    openapi_schema = get_openapi(
        title="PureWater API",
        version="0.0.1",
        description="API для сервиса отслеживания качества воды",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema

    yield

    await fast_mqtt.mqtt_shutdown()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins='*',
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
