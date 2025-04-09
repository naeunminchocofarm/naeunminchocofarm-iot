from air_temp_humidity_sensor import AirTempHumiditySensor
from led_actuator import LedActuator
import time

class Controller:
  def __init__(self, air_temp_humid_sensor):
    self.air_temp_humid_sensor = air_temp_humid_sensor

  @staticmethod
  def from_config(config = {}):


s = AirTempHumiditySensor.from_config({
  "type": "air_temp_humid",
  "intervalSeconds": 1,
  "gpio": 27
})

a = LedActuator.from_config({
  "type": "led",
  "gpio": 17
})

s.start()
a.start()
s.subscribe(lambda v: a.apply({"led": v.get("air_temp", 0.0) >= 24.0}))

time.sleep(6)

s.exit()
a.exit()