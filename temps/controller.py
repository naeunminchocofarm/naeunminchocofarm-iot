from air_temp_humidity_sensor import AirTempHumiditySensor
from led_actuator import LedActuator
import time
from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory

class Controller:
  def __init__(self, sensors = [], actuators = []):
    self.sensors = {}
    for sensor in sensors:
      self.sensors.setdefault(sensor.type, []).append(sensor)

    self.actuators = {}
    for actuator in actuators:
      self.actuators.setdefault(actuator.type, []).append(actuator)

  @staticmethod
  def from_config(config = {}):
    sensors = list(map(SensorFactory.create_sensor, config.get("sensors", [])))
    actuators = list(map(ActuatorFactory.create_actuator, config.get("actuators", [])))
    return Controller(sensors, actuators)


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