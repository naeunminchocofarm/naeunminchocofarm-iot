from ncf_api_server import NcfApiServer
from bmp180 import Bmp180
import time

def run():
    apiServer = NcfApiServer()
    b180 = Bmp180()
    temperature = b180.read_temperature()
    apiServer.insertTemperature(temperature)
        
run()
  