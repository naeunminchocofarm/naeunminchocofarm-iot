from .sensor import Sensor
from ncf_api_server import NcfApiServer
from adc import Adc
import datetime
import requests

class AdcSensor(Sensor):
  def __init__(self, farm_name, crops_name, section_name, config):
    super().__init__(farm_name, crops_name, section_name, config)
    self.adc = Adc()
    self.enabled_sunshine = self._get_enable_sunshine()
    self.sunshine_channel = self._get_sunshine_channel()
    self.enabled_soil_moisture = self._get_enable_soil_moisture()
    self.soil_moisture_channel = self._get_soil_moisture_channel()
    self.interval_seconds = self._get_interval_seconds()

  def start(self):
    self.api_server = NcfApiServer()
    self.exec_datetime = datetime.datetime.now()

  def loop(self):
    now = datetime.datetime.now()
    if now < self.exec_datetime:
      return
    
    try:
      self._api_sunshine_value()
      self._api_soil_moisture_value()
    except requests.exceptions.ConnectionError as e:
      print(type(e))
      print(e)
    finally:
      self.exec_datetime = now + datetime.timedelta(seconds=self.interval_seconds)

  def exit(self):
    pass

  def _api_sunshine_value(self):
    if not self.enabled_sunshine:
      return
    sunshine_value = self.adc.read_channel(self.sunshine_channel)
    print('Sunshine: {}'.format(sunshine_value))
    position = self.get_position()
    self.api_server.insert_sunshine_value(sunshine_value, position)

  def _api_soil_moisture_value(self):
    if not self.enabled_soil_moisture:
      return
    soil_moisture_value = self.adc.read_channel(self.soil_moisture_channel)
    print('Soil moisture: {}'.format(soil_moisture_value))
    position = self.get_position()
    self.api_server.insert_soil_moisture_value(soil_moisture_value, position)

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