from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod

class Controller(ABC):
  def __init__(self, uuid, sensors = [], actuators = []):
    self.uuid = uuid
    self.sensors = {}
    for sensor in sensors:
      self.sensors[sensor.type] = sensor

    self.actuators = {}
    for actuator in actuators:
      self.actuators[actuator.type] = actuator

  @staticmethod
  def get_uuid(config = {}):
    result = config.get('uuid')
    if not result:
      raise TypeError('controller uuid cannot be empty')
    return result
  
  @staticmethod
  def get_sensors(config = {}):
    return list(map(SensorFactory.create_sensor, config.get("sensors", [])))
  
  @staticmethod
  def get_actuators(config = {}):
    return list(map(ActuatorFactory.create_actuator, config.get("actuators", [])))
  
  def start(self):
    for sensor in self.sensors.values():
      sensor.subscribe(self._on_sensor_value)

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

  @abstractmethod
  def _init_resources(self):
    pass
  
  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _on_sensor_value(self, value, type, uuid):
    pass