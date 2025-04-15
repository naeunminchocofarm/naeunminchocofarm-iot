from actuator import Actuator
import RPi.GPIO as GPIO
import datetime
import pytz

class LedActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.power = 'off'
    self.is_ready = False

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.OUT)
    self.is_ready = True

  def exit(self):
    self.is_ready = False
    GPIO.cleanup()

  def command(self, action, parameters=[]):
    if not self.is_ready:
      raise RuntimeError("Actuator must be started before command")
    match action:
      case "on":
        self.turn_on()
      case "off":
        self.turn_off()

  def turn_on(self):
    self.power = 'on'
    GPIO.output(self.gpio, 1)

  def turn_off(self):
    self.power = 'off'
    GPIO.output(self.gpio, 0)

  def read(self):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "power": self.power
    }
  
  def read_datas(self):
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    return [
      {
        "name": "power",
        "value": self.power,
        "measured-at": measured_at,
        "uuid": self.uuid,
        "type": self.type
      }
    ]
  
  @staticmethod
  def from_config(config: dict):
    type = Actuator.get_type(config)
    uuid = Actuator.get_uuid(config)
    gpio = LedActuator._get_gpio(config)
    return LedActuator(type, uuid, gpio)

  @staticmethod
  def _get_gpio(config = {}):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError('led actuator gpio cannot be empty')
    return result