from .sensor import Sensor
from ncf_api_server import NcfApiServer
import time
import threading
from adc import Adc

class AdcSensor(Sensor):
  def __init__(self, farm_name, crops_name, section_name, config):
    super().__init__(farm_name, crops_name, section_name, config)
    self.interval_thread = threading.Thread(target=self._handle_interval)
    self.stop_interval_event = threading.Event()
    self.adc = Adc()
    self.enabled_sunshine = self._get_enable_sunshine()
    self.sunshine_channel = self._get_sunshine_channel()
    self.enabled_soil_moisture = self._get_enable_soil_moisture()
    self.soil_moisture_channel = self._get_soil_moisture_channel()
    self.interval_seconds = self._get_interval_seconds()

  def run(self):
    self.interval_thread.start()

  def exit(self):
    self.stop_interval_event.set()
    self.interval_thread.join()

  def rerun(self):
    pass

  def _handle_interval(self):
    api_server = NcfApiServer()
    while not self.stop_interval_event.is_set():
      self._api_sunshine_value(api_server)
      self._api_soil_moisture_value(api_server)

      time.sleep(self.interval_seconds)

  def _api_sunshine_value(self, api_server):
    if not self.enabled_sunshine:
      return
    sunshine_value = self.adc.read_channel(self.sunshine_channel)
    print('Sunshine: {}'.format(sunshine_value))
    api_server.insert_sunshine_value(sunshine_value, self.farm_name, self.crops_name, self.section_name, self.name)

  def _api_soil_moisture_value(self, api_server):
    if not self.enabled_soil_moisture:
      return
    soil_moisture_value = self.adc.read_channel(self.soil_moisture_channel)
    print('Soil moisture: {}'.format(soil_moisture_value))
    api_server.insert_soil_moisture_value(soil_moisture_value, self.farm_name, self.crops_name, self.section_name, self.name)

  def _get_enable_sunshine(self):
    result = self.config.get('enableSunshine', False)
    return result
  
  def _get_sunshine_channel(self):
    result = self.config.get('sunshineChannel', None)
    if result is None:
      raise TypeError('sunshine channel cannot be empty.')
    return result
  
  def _get_enable_soil_moisture(self):
    result = self.config.get('enableSoilMoisture', False)
    return result
  
  def _get_soil_moisture_channel(self):
    result = self.config.get('soilMoistureChannel', None)
    if result is None:
      raise TypeError('soil moisture channel cannot be empty.')
    return result
  
  def _get_interval_seconds(self):
    result = self.config.get('intervalSeconds', 600)
    return result