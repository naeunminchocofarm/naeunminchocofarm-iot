from .actuator import Actuator
import RPi.GPIO as GPIO
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS
from application_config_manager import ApplicationConfigManager

class LedActuator(Actuator):
  def __init__(self, config):
    super().__init__()
    self.gpio = self._get_gpio()
    self.is_on = False

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.OUT)

    def _on_open(subs):
      subs.subscribe()

    def _on_message(subs, frame):
      if frame.body == 'read-status':
        res = 'led-on' if self.is_on else 'led-off'
        subs.send(body=res)

    application_config_manager = ApplicationConfigManager()
    subscriber = NcfSubscriber(application_config_manager.websocket_path, self.uuid)
    subscriber.on_open = _on_open
    subscriber.on_message = _on_message
    subscriber.connect()
    self.subscriber = subscriber

  def loop(self):
    pass

  def exit(self):
    self.subscriber.close()

  def _get_gpio(self):
    result = self.config.get('gpio', None)
    if result is None:
      raise TypeError('let actuator gpio cannot be empty')
    return result