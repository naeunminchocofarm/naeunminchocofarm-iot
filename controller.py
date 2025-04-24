from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod

class Controller(ABC):
  def __init__(self, type, uuid, sensors = [], actuators = []):
    self.type = type
    self.uuid = uuid
    self.sensors = {}
    for sensor in sensors:
      self.sensors[sensor.type] = sensor
    self.actuators = {}
    for actuator in actuators:
      self.actuators[actuator.type] = actuator
    self.settings = {}
    self.sensor_channel_subscribers = []

  @abstractmethod
  def start(self):
    pass
    
  @abstractmethod
  def exit(self):
    pass

  @abstractmethod
  def read_sensor_datas(self):
    pass

  @abstractmethod
  def read_actuator_datas(self):
    pass

  @abstractmethod
  def get_status(self):
    pass

  @abstractmethod
  def control(self):
    pass

  def subscribe_status(self, callback):
    self.sensor_channel_subscribers.append(callback)
    return lambda: self.sensor_channel_subscribers.remove(callback)
  
  def notify_status(self, data):
    for callback in self.sensor_channel_subscribers:
      callback(data)
  
  def update_settings(self, settings):
    self.settings.update(settings)

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