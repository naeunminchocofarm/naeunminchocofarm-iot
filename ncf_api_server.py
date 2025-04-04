import requests
from datetime import datetime
import pytz

API_SERVER_PATH = "http://192.168.30.128:8080"
TEST_API_SERVER_PATH = "http://192.168.30.128:8081"

class NcfApiServer:
    def __init__(self):
        None
        
    def login(self, id, roleNames, roleFlags):
        r = requests.post(f'{API_SERVER_PATH}/examples/login', data={'id': 2, 'roleNames': 'normal', 'roleFlags': 11})
        return r.text

    def insertTemperature(self, temperature):
        payload = {
            "temperature": temperature,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        }
        r = requests.post(f"{API_SERVER_PATH}/temperatures", data=payload)
        
    def insertLdrValue(self, ldr_value):
        payload = {
            "ldr-value": ldr_value,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        }
        requests.post(f"{API_SERVER_PATH}/ldr-values", data=payload)

    def insertSoilMoistureValue(self, value):
        payload = {
            "soil-moisture-value": value,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        }
        requests.post(f"{API_SERVER_PATH}/soil-moisture-values", data=payload)
    
    def insertHumidity(self, humidity_percentage):
        payload = {
            "humidity-percentage": humidity_percentage,
            "measured-at": datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        }
        requests.post(f"{API_SERVER_PATH}/humidities", data=payload)

    def insert_air_temperature(self, temperature_c, position):
        payload = position
        payload['temperature-c'] = temperature_c
        payload['measured-at'] = datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        requests.post(f'{TEST_API_SERVER_PATH}/air-temperatures/v2', data=payload)

    def insert_humidity(self, humidity_percentage, position):
        payload = position
        payload['humidity-percentage'] = humidity_percentage
        payload['measured-at'] = datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        requests.post(f'{TEST_API_SERVER_PATH}/humidities/v2', data=payload)

    def insert_sunshine_value(self, sunshine_value, position):
        payload = position
        payload['sunshine-value'] = sunshine_value
        payload['measured-at'] = datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        requests.post(f'{TEST_API_SERVER_PATH}/sunshines/v2', data=payload)

    def insert_soil_moisture_value(self, soil_moisture_value, position):
        payload = position
        payload['soil-moisture-value'] = soil_moisture_value
        payload['measured-at'] = datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
        requests.post(f'{TEST_API_SERVER_PATH}/soil-moistures/v2', data=payload)