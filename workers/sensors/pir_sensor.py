from .sensor import Sensor
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS
import RPi.GPIO as GPIO
import datetime

class PirSensor(Sensor):
  def __init__(self, farm_name, crops_name, section_name, config):
    super().__init__(farm_name, crops_name, section_name, config)
    self.realtime_seconds = self._get_realtime_seconds()
    self.gpio = self._get_gpio()

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.subscriber = NcfSubscriber(WEB_SOCKET_PATHS['dev'], DESTINATIONS['motion'])
    self.subscriber.connect()
    self.exec_datetime = datetime.datetime.now() + datetime.timedelta(seconds=5)

  def loop(self):
    now = datetime.datetime.now()
    if now < self.exec_datetime:
      return
    
    if GPIO.input(self.gpio) == 1:
      print('motion detected!')
      self.subscriber.send(body='detected')

  def exit(self):
    GPIO.cleanup()
    self.subscriber.close()

  def _get_realtime_seconds(self):
    result = self.config.get('realtimeSeconds', 1)
    return result
  
  def _get_gpio(self):
    result = self.config.get('gpio', None)
    if result is None:
      raise TypeError('gpio cannot be empty.')
    return result