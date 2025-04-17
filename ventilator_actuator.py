from actuator import Actuator
import RPi.GPIO as GPIO
import datetime
import pytz
import threading
import time

class VentilatorActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.power = 'off'
    self.is_ready = False
    self.servo = None

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.OUT)
    self.servo = GPIO.PWM(self.gpio,50)
    self.servo.start(0)
    self.is_ready = True

  def exit(self):
    self.is_ready = False
    self.servo.stop()
    GPIO.cleanup()

  def _manual_on(self, delay = 0.5):
    self.servo.ChangeDutyCycle(7.5)
    self.power = 'on'
    time.sleep(delay)
    self.servo.ChangeDutyCycle(0)    

  def _manual_off(self, delay=0.5):
    self.servo.ChangeDutyCycle(2.5)
    self.power = 'off'
    time.sleep(delay)
    self.servo.ChangeDutyCycle(0)

  def command(self, action, parameters=[]):
    if not self.is_ready:
      raise RuntimeError("Actuator must be started before command")
    if self.power == action:
      return
    match action:
      case "on":
        self.power = 'on'
        threading.Thread(target=self._manual_on, args=(1,), daemon=True).start()

      case "off":
        self.power = 'off'
        threading.Thread(target=self._manual_off, args=(1,), daemon=True).start()

  def read_datas(self):
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    return [
      {
        "name": "ventilator_power",
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
    gpio = VentilatorActuator._get_gpio(config)
    return VentilatorActuator(type, uuid, gpio)

  @staticmethod
  def _get_gpio(config = {}):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError('ventilator actuator gpio cannot be empty')
    return result