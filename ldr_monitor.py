from ncf_api_server import NcfApiServer
from adc import Adc

LDR_CHANNEL = 0

def run():
    adc = Adc()
    ldr_value = adc.read_channel(LDR_CHANNEL)
    apiServer = NcfApiServer()
    apiServer.insertLdrValue(ldr_value)
    print(ldr_value)
    
run()