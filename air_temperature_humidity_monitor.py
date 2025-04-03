import board
import adafruit_dht
from ncf_api_server import NcfApiServer

dhtDevice = adafruit_dht.DHT22(board.D27)

try:
    temperature_c = dhtDevice.temperature
    humidity = dhtDevice.humidity
    print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity))
    api_server = NcfApiServer()
    api_server.insertTemperature(temperature_c)
    api_server.insertHumidity(humidity)
except RuntimeError as err:
    print(err)
except:
    print('error!')
finally:
    dhtDevice.exit()
