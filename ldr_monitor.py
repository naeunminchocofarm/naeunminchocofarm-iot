from ncf_api_server import NcfApiServer
from adc import Adc

def run():
    adc = Adc()
    ldr_value = adc.read_ldr_value()
    apiServer = NcfApiServer()
    apiServer.insertLdrValue(ldr_value)
    print(ldr_value)
    
run()