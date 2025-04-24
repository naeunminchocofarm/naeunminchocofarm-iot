from sensor import Sensor
import RPi.GPIO as GPIO
import datetime
import pytz
import threading
import time

class PirSensor(Sensor):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.is_ready = False
    self.gpio = gpio
    self.stop_event = threading.Event()
    self.current_datas = []
    self.measure_thread = None

  def start(self):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(self.gpio, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    self.stop_event.clear()
    self.measure_thread = threading.Thread(target=self._measure_data, daemon=True)
    self.measure_thread.start()
    self.is_ready = True
    print('pir is ready')
  
  def exit(self):
    self.is_ready = False
    self.stop_event.set()
    if self.measure_thread is not None:
      self.measure_thread.join()
    GPIO.cleanup()
  
  def read_datas(self):
    return self.current_datas.copy()
  
  def _measure_data(self):
    INTERVAL_SECONDS = 0.4
    exec_time = time.time()
    while not self.stop_event.is_set() and self.is_ready:
      exec_time += INTERVAL_SECONDS
      time.sleep(exec_time - time.time())
      measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
      IS_DETECTED = self.is_detected()
      self.current_datas = [
        {
          "name": "motion",
          "value": 'detected' if IS_DETECTED else 'not-detected',
          "measured-at": measured_at,
          "uuid": self.uuid,
          "type": self.type
        }
      ]
      if (IS_DETECTED):
        self.notify(self.current_datas.copy())
  
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
