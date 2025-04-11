import requests

class NcfApiServer:
    def __init__(self):
        pass

    def send_sensor_datas(self, sensor_datas, host):
        requests.post(url=f'{host}/sensors/datas', json=sensor_datas)