from sensor import Sensor
import RPi.GPIO as GPIO
import datetime
import pytz

class PirSensor(Sensor):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.is_ready = False
    self.gpio = gpio

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.is_ready = True
  
  def exit(self):
    self.is_ready = False
    GPIO.cleanup()
  
  def read(self):
    if not self.is_ready:
      return {}
    return {
      "type": self.type,
      "uuid": self.uuid,
      "motion": 'detected' if self.is_detected() else 'not-detected'
    }
  
  def read_datas(self):
    if not self.is_ready:
      return []
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    return [
      {
        "name": "motion",
        "value": 'detected' if self.is_detected() else 'not-detected',
        "measured-at": measured_at,
        "uuid": self.uuid,
        "type": self.type
      }
    ]
  
  def is_detected(self):
    return GPIO.input(self.gpio) == 1
  
  @staticmethod
  def from_config(config = {}):
    type = Sensor.get_type(config)
    uuid = Sensor.get_uuid(config)
    gpio = PirSensor.get_gpio(config)
    return PirSensor(type, uuid, gpio)
  
  @staticmethod
  def get_gpio(config = {}):
    result = config.get('gpio')
    if result is None:
      raise TypeError('pir sensor gpio cannot be empty')
    return result