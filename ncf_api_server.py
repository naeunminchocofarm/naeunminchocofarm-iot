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
