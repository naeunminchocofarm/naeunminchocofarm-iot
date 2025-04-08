from .sensor import Sensor
from ncf_api_server import NcfApiServer
import board
import adafruit_dht
import datetime
import requests

class AirTemperatureHumiditySensor(Sensor):
  def __init__(self, config):
    super().__init__(config)
    self.interval_seconds = self._get_interval_seconds()

  def start(self):
    self.api_server = NcfApiServer()
    self.exec_datetime = datetime.datetime.now() + datetime.timedelta(seconds=5)
    self.dhtDevice = self._createDhtDevice()

  def loop(self):
    now = datetime.datetime.now()
    if now < self.exec_datetime:
      return
    try:
      temperature_c = self.dhtDevice.temperature
      humidity_percentage = self.dhtDevice.humidity
      print("Temp: {:.1f} C    Humidity: {:.1f}% ".format(temperature_c, humidity_percentage))
      self.api_server.insert_air_temperature_v2(temperature_c, self.uuid)
      self.api_server.insert_humidity_v2(humidity_percentage, self.uuid)
      self.exec_datetime = now + datetime.timedelta(seconds=self.interval_seconds)
    except RuntimeError as e:
      print(type(e))
      print(e)
    except TypeError as e:
      print(type(e))
      print(e)
    except requests.exceptions.ConnectionError as e:
      print(type(e))
      print(e)
      self.exec_datetime = now + datetime.timedelta(seconds=self.interval_seconds)

  def exit(self):
    self.dhtDevice.exit()

  def _createDhtDevice(self):
    pin_num = self.config.get('gpio', None)
    if pin_num is None: 
      raise TypeError('gpio pin cannot be empty.')
    pin_key = 'D{}'.format(pin_num)
    pin = getattr(board, pin_key)
    result = adafruit_dht.DHT22(pin)
    return result
  
  def _get_interval_seconds(self):
    result = self.config.get('intervalSeconds', 600)
    return result
