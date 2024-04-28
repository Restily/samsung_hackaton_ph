import json
from typing import Any

from fastapi_mqtt import MQTTConfig
from gmqtt import Client as MQTTClient
from fastapi_mqtt import FastMQTT

from database import DBWorker
from models import DeviceLog
from utils import write_device_log, SENSOR_TYPE_KEYS


mqtt_config = MQTTConfig()

fast_mqtt = FastMQTT(config=mqtt_config)


@fast_mqtt.on_connect()
def connect(client: MQTTClient, flags: int, rc: int, properties: Any):
    client.subscribe("TestTopic")
    print("Connected: ", client, flags, rc, properties)


@fast_mqtt.on_message()
async def message(client: MQTTClient, topic: str, payload: bytes, qos: int, properties: Any):
    print("Received message: ", topic, payload.decode(), qos, properties)
    json_data = json.loads(payload.decode())

    sql = """
        SELECT device_id
        FROM device
        WHERE device_name = $1::text
    """
    device_info = await DBWorker.fetch(sql, json_data['device_name'])
    device_id = device_info[0]['device_id']

    for sensor_data in json_data['sensordatavalues']:
        data = DeviceLog(time=json_data['device_timestamp'],
                         device_id=device_id,
                         value=float(sensor_data['value']))

        await write_device_log(data)


@fast_mqtt.on_disconnect()
def disconnect(client: MQTTClient, packet, exc=None):
    print("Disconnected")


@fast_mqtt.on_subscribe()
def subscribe(client: MQTTClient, mid: int, qos: int, properties: Any):
    print("Subscribed", client, mid, qos, properties)
