from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod

class Controller(ABC):
  def __init__(self, type, uuid, settings, sensors = [], actuators = [], interval_seconds=60):
    self.type = type
    self.uuid = uuid
    self.sensors = {}
    for sensor in sensors:
      self.sensors[sensor.type] = sensor
    self.actuators = {}
    for actuator in actuators:
      self.actuators[actuator.type] = actuator
    self.interval_seconds = interval_seconds
    self.settings = settings

  @staticmethod
  def get_type(config = {}):
    result = config.get("type")
    if not result:
      raise TypeError('controller type cannot be empty')
    return result

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
  
  @staticmethod
  def get_interval_seconds(config = {}):
    return config.get("intervalSeconds", 60)
  
  @abstractmethod
  def start(self):
    pass
    
  @abstractmethod
  def exit(self):
    pass

  @abstractmethod
  def command(self, actuator_type, action, parameters = {}):
    pass
  
  @abstractmethod
  def read(self) -> dict:
    pass