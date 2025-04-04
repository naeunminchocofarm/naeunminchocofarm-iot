from .sensor import Sensor
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS
import RPi.GPIO as GPIO
import datetime

class PirSensor(Sensor):
  def __init__(self, farm_name, crops_name, section_name, config):
    super().__init__(farm_name, crops_name, section_name, config)
    self.realtime_seconds = self._get_realtime_seconds()

  def start(self):
    self.exec_datetime = datetime.datetime.now()
    pass

  def loop(self):
    now = datetime.datetime.now()
    if now < self.exec_datetime:
      return
    self.exec_datetime = now + datetime.timedelta(seconds=self.realtime_seconds)
    print('pir sensor!')
    pass

  def exit(self):
    pass

  def _get_realtime_seconds(self):
    result = self.config.get('realtimeSeconds', 1)
    return result