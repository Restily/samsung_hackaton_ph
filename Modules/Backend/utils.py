from enum import IntEnum
import pickle

import numpy

from database import DBWorker


class SensorType(IntEnum):
    WATER_PH = 0


SENSOR_TYPE_KEYS = {
    'PH': SensorType.WATER_PH
}


async def write_device_log(data):
    sql = """
        INSERT INTO device_log (time, device_id, value)
        VALUES ($1::timestamp, $2::int, $3::double precision)
    """
    await DBWorker.execute(sql, data.time.replace(microsecond=0, tzinfo=None),
                           data.device_id, data.value)

    predict_data = numpy.array(data.value).reshape(-1, 1)
    danger_type = PredictModel.predict(predict_data)

    sql = """
        UPDATE device
        SET properties = $2::jsonb
        WHERE device_id = $1::int
    """
    await DBWorker.execute(sql, data.device_id, 
                           {'last_value': data.value, 'danger_type': danger_type})


class PredictModel:

    model = None

    @classmethod
    def load_model(cls):
        cls.model = pickle.load(open('model.sav', 'rb'))

    @classmethod
    def predict(cls, value: float):
        predict_value = cls.model.predict(value)

        return int(predict_value[0])
    
