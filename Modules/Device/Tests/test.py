import json
import random
import time
import paho.mqtt.client as mqtt

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.connect("localhost")

client.loop_start()

step = 0
while True:
    data = json.dumps({
        'device_timestamp': f'2024-04-28T15:{10 + step}:47.340Z',
        'device_name': 'device_1',
        'sensor_model': 'sds011',
        'location': [{'latitude': '55.796441'}, {'longitude': '37.600502'}],
        'sensordatavalues': [{'value_type': 'PH', 'value': random.randrange(4, 6) + random.random()}]
    })
    client.publish("TestTopic", data)
    step += 5
    time.sleep(3)

client.loop_stop()

# mosquitto.exe -v
