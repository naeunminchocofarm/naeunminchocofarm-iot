from ncf_api_server import NcfApiServer
from adc import Adc

SOIL_MOISTURE_CHANNEL = 1

def run():
    adc = Adc()
    soil_moisture_value = 1023 - adc.read_channel(SOIL_MOISTURE_CHANNEL)
    apiServer = NcfApiServer()
    apiServer.insertSoilMoistureValue(soil_moisture_value)
    print(soil_moisture_value)
    
run()
