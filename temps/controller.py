from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod

class Controller(ABC):
  def __init__(self, type, uuid, sensors = [], actuators = []):
    self.type = type
    self.uuid = uuid
    self.subscribers = []
    self.sensors = {}
    for sensor in sensors:
      self.sensors[sensor.type] = sensor
    self.actuators = {}
    for actuator in actuators:
      self.actuators[actuator.type] = actuator

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
  
  def subscribe(self, callback):
    self.subscribers.append(callback)

  def _notify(self, value):
    for callback in self.subscribers:
      callback(value, self.type, self.uuid)

  def _handle_sensor_value(self, value, type, uuid):
    self._on_sensor_value(value, type, uuid)
    self._notify({
      "sensor_value": value,
      "sensor_type": type,
      "sensor_uuid": uuid
    }, self.type, self.uuid)
  
  def start(self):
    self._init_resources()
    for sensor in self.sensors.values():
      try:
        sensor.subscribe(self._handle_sensor_value)
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