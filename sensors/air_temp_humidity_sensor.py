from .sensor import Sensor
from ..ncf_api_server import NcfApiServer
import board
import adafruit_dht

class AirTemperatureHumiditySensor(Sensor):
  def __init__(self, dict):
    super().__init__(dict)
    self.dhtDevice = self._createDhtDevice()

  def run(self):
    try:
      temperature_c = self.dhtDevice.temperature
      humidity_percentage = self.dhtDevice.humidity
      print("Temp: {:.1f} C    Humidity: {}% ".format(temperature_c, humidity_percentage))
      # api_server = NcfApiServer()
      # api_server.insertTemperature(temperature_c)
      # api_server.insertHumidity(humidity_percentage)
    except:
      print('error')
    finally:
      self.dhtDevice.exit()

  def rerun(self):
    pass

  def exit(self):
    pass

  def _createDhtDevice(self):
    pin_num = self.config.get('gpio', None)
    if pin_num is None: 
      raise TypeError('gpio pin cannot be empty.')
    pin_key = 'D{}'.format(pin_num)
    pin = getattr(board, pin_key)
    result = adafruit_dht.DHT22(pin)
    return result