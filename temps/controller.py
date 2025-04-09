from sensor_factory import SensorFactory
from actuator_factory import ActuatorFactory
from abc import ABC, abstractmethod
import threading
import time

class Controller(ABC):
  def __init__(self, type, uuid, sensors = [], actuators = [], interval_seconds=60):
    self.type = type
    self.uuid = uuid
    self.subscribers = []
    self.sensors = {}
    self.values = {}
    self.stop_notify_loop = threading.Event()
    self.values_lock = threading.Lock()
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
  
  def subscribe(self, callback):
    self.subscribers.append(callback)

  def _notify(self, value):
    for callback in self.subscribers:
      callback(value, self.type, self.uuid)

  def _handle_sensor_value(self, value, type, uuid):
    with self.values_lock:
      self.values.update(value)
    self._on_sensor_value(value, type, uuid)
  
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
    self.stop_notify_loop.clear()
    threading.Thread(target=self._notify_loop).start()
    
  def exit(self):
    self.stop_notify_loop.set()
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

  def _notify_loop(self):
    next_time = time.time()
    while not self.stop_notify_loop.is_set():
      if next_time <= time.time():
        with self.values_lock:
          snapshot = self.values.copy()
        self._notify(snapshot)
        next_time += self.interval_seconds
      time.sleep(1)

  def command(self, actuator_type, action, parameters = {}):
    if actuator_type in self.actuators:
      self.actuators[actuator_type].command(action, parameters)

  @abstractmethod
  def _init_resources(self):
    pass
  
  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _on_sensor_value(self, value, type, uuid):
    pass