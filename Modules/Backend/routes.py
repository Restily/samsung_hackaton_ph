import datetime
from fastapi import APIRouter, Depends

import models
from database import DBWorker
from utils import write_device_log


data_router = APIRouter()


@data_router.post(
    '/write_data',
    summary='Запись данных с датчика'
)
async def write_data(data: models.DeviceLog):
    write_device_log(data)


@data_router.get(
    '/all',
    summary='Получение данных по всем датчикам'
)
async def all_devices() -> list[models.DeviceData]:
    sql = """
        SELECT
            d.device_id,
            d.active,
            d.device_name,
            d.name,
            d.latitude,
            d.longitude,
            d.active,
            (d.properties->>'last_value')::double precision as last_value,
            (d.properties->>'danger_type')::int as danger_type,
            (
                CASE WHEN p.hidden THEN
                    null::jsonb
                ELSE
                    jsonb_build_object(
                        'person_id', p.person_id,
                        'name', p.name,
                        'surname', p.surname
                    )
                END
            ) as person_data
        FROM device d
        JOIN person p USING (person_id)
    """
    data = await DBWorker.fetch(sql)

    return data


@data_router.get(
    '/graph_data',
    summary='Получение данных для построение графикаы'
)
async def graph_data(graph_params: models.GraphParams = Depends()) -> list[models.GraphPoint]:
    if graph_params.start_time is None:
        graph_params.start_time = datetime.datetime.now()

    if graph_params.end_time is None:
        graph_params.end_time = datetime.datetime.now() - datetime.timedelta(days=30)

    sql = f"""
        SELECT 
            time_bucket('{graph_params.interval}', time) as time,
            avg(value) as value
        FROM device_log
        WHERE device_id = $1::int
            AND time <= $2::timestamp
            AND time >= $3::timestamp
        GROUP BY time
        ORDER BY time DESC LIMIT 50
    """
    graph_data = await DBWorker.fetch(sql,
                                      graph_params.device_id,
                                      graph_params.start_time,
                                      graph_params.end_time)

    return graph_data
