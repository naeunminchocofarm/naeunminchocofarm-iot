import time
from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory

class Controller:
  def __init__(self, sensors = [], actuators = []):
    self.sensors = {}
    for sensor in sensors:
      self.sensors[sensor.type] = sensor

    self.actuators = {}
    for actuator in actuators:
      self.actuators[actuator.type] = actuator

  @staticmethod
  def from_config(config = {}):
    sensors = list(map(SensorFactory.create_sensor, config.get("sensors", [])))
    actuators = list(map(ActuatorFactory.create_actuator, config.get("actuators", [])))
    return Controller(sensors, actuators)
  
  def start(self):
    self._init_resources()

    for sensor in self.sensors.values():
      try:
        sensor.start()
      except TypeError as err:
        print(type(err))
        print(err)

    for actuator in self.actuators.values():
      try:
        actuator.start()
      except TypeError as err:
        print(type(err))
        print(err)
    
  def exit(self):
    for sensor in self.sensors.values():
      try:
        sensor.exit()
      except:
        continue

    for actuator in self.actuators.values():
      try:
        actuator.exit()
      except:
        continue

    self._cleanup_resources()

  def _init_resources(self):
    for sensor in self.sensors.values():
      sensor.subscribe(self._on_sensor_value)

  def _cleanup_resources(self):
    pass

  def _on_sensor_value(self, value, type, uuid):
    pass

sensors_config = [
  {
    "type": "air_temp_humid",
    "uuid": "test-uuid-1",
    "intervalSeconds": 1,
    "gpio": 27
  }
]

actuators_config = [
  {
    "type": "led",
    "uuid": "test-uuid-2",
    "gpio": 17
  }
]

controller_config = {
  "sensors": sensors_config,
  "actuators": actuators_config
}

c = Controller.from_config(controller_config);
c.start()
time.sleep(6)
c.exit()