from actuator import Actuator
import RPi.GPIO as GPIO
import datetime
import pytz

class BuzzerActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.power = 'off'
    self.is_ready = False
    self.buzzer = None
    self.speed = 0.5

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.OUT)
    self.buzzer = GPIO.PWM(self.gpio, 400)
    self.is_ready = True

  def exit(self):
    self.is_ready = False
    GPIO.cleanup()

  def command(self, action, parameters=[]):
    if not self.is_ready:
      raise RuntimeError("Actuator must be started before command")
    match action:
      case 'on':
        self.buzzer.start(10)
      case 'off':
        self.buzzer.stop()
      
  def read_datas(self):
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    return [
      {
        "name": "buzzer_power",
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
    gpio = BuzzerActuator._get_gpio(config)
    return BuzzerActuator(type, uuid, gpio)

  @staticmethod
  def _get_gpio(config = {}):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError('buzzer actuator gpio cannot be empty')
    return result