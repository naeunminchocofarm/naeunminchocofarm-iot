import requests
from datetime import datetime
import pytz

API_SERVER_PATH = "http://192.168.30.128:8080"
TEST_API_SERVER_PATH = "http://192.168.30.128:8081"

class NcfApiServer:
    def __init__(self):
        pass

    def insert_air_temperature_v2(self, temperature_c, sensor_uuid):
        payload = {
            "temperature-c": temperature_c,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat(),
            "sensor-uuid": sensor_uuid
        }
        requests.post(f'{API_SERVER_PATH}/air-temperatures/v3', data=payload)

    def insert_humidity_v2(self, humidity_percentage, sensor_uuid):
        payload = {
            "humidity-percentage": humidity_percentage,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat(),
            "sensor-uuid": sensor_uuid
        }
        requests.post(f'{API_SERVER_PATH}/humidities/v3', data=payload)

    def insert_sunshine_value_v2(self, sunshine_value, sensor_uuid):
        payload = {
            "sunshine-value": sunshine_value,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat(),
            "sensor-uuid": sensor_uuid
        }
        requests.post(f'{API_SERVER_PATH}/sunshines/v3', data=payload)

    def insert_soil_moisture_value_v2(self, soil_moisture_value, sensor_uuid):
        payload = {
            "soil-moisture-value": soil_moisture_value,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat(),
            "sensor-uuid": sensor_uuid
        }
        requests.post(f'{API_SERVER_PATH}/soil-moistures/v3', data=payload)
