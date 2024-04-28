from datetime import datetime
from pydantic import BaseModel, Field

from utils import SensorType


class DeviceLog(BaseModel):
    time: datetime
    device_id: int
    value: float


class GraphParams(BaseModel):
    device_id: int
    type: int = Field(SensorType.WATER_PH)
    start_time: datetime | None = Field(None)
    end_time: datetime | None = Field(None)
    interval: str | None = Field('5 minutes')


class GraphPoint(BaseModel):
    time: datetime
    value: float


class DeviceData(BaseModel):
    device_id: int
    last_value: float | None
    danger_type: int | None
    active: bool
    device_name: str
    name: str
    latitude: float
    longitude: float
    person_data: dict | None
