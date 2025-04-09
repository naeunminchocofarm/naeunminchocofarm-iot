from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod

class Controller(ABC):
  def __init__(self, type, uuid, sensors = [], actuators = [], interval_seconds=60):
    self.type = type
    self.uuid = uuid
    self.sensors = {}
    self.sensors_status = {}
    self.interval_seconds = interval_seconds
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
  
  @staticmethod
  def get_interval_seconds(config = {}):
    return config.get("intervalSeconds", 60)
  
  def _handle_sensor_value(self, value, type, uuid):
    value.update({
      "uuid": uuid
    })
    self.sensors_status[type] = value
    # self._on_sensor_value(value, type, uuid)
  
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

  def command(self, actuator_type, action, parameters = {}):
    if actuator_type in self.actuators:
      self.actuators[actuator_type].command(action, parameters)
  
  def read(self) -> dict:
    actuators_status = {}
    for actuator in self.actuators.values():
      status = actuator.read()
      status.update({
        "uuid": actuator.uuid
      })
      actuators_status[actuator.type] = status
    result = {
      "sensors": self.sensors_status,
      "actuators": actuators_status
    }
    return result

  @abstractmethod
  def _init_resources(self):
    pass
  
  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _on_sensor_value(self, value, type, uuid):
    pass