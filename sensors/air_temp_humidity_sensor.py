from .sensor import Sensor
from ncf_api_server import NcfApiServer
import board
import adafruit_dht
import time
import threading

class AirTemperatureHumiditySensor(Sensor):
  def __init__(self, farm_name, crops_name, section_name, config):
    super().__init__(farm_name, crops_name, section_name, config)
    self.dhtDevice = self._createDhtDevice()
    self.interval_seconds = self._get_interval_seconds()
    self.interval_thread = threading.Thread(target=self._handle_interval)
    self.stop_interval_event = threading.Event()

  def run(self):
      self.interval_thread.start()

  def _handle_interval(self):
      api_server = NcfApiServer()
      while not self.stop_interval_event.is_set():
        temperature_c = self.dhtDevice.temperature
        humidity_percentage = self.dhtDevice.humidity
        print("Temp: {:.1f} C    Humidity: {:.1f}% ".format(temperature_c, humidity_percentage))
        
        api_server.insert_air_temperature(temperature_c, self.farm_name, self.crops_name, self.section_name, self.name)

        api_server.insert_humidity(humidity_percentage, self.farm_name, self.crops_name, self.section_name, self.name)

        time.sleep(self.interval_seconds)
  
  def rerun(self):
    pass

  def exit(self):
    self.dhtDevice.exit()
    self.stop_interval_event.set()
    self.interval_thread.join()

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