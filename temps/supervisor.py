from controller_factory import ControllerFactory
from abc import ABC, abstractmethod

class Supervisor(ABC):
  def __init__(self, type, uuid, controllers, interval_seconds):
    self.type = type
    self.uuid = uuid
    self.controllers = controllers
    self.interval_seconds = interval_seconds

  @staticmethod
  def get_type(config = {}):
    result = config.get("type")
    if not result:
      raise TypeError('supervisor type cannot be empty')
    return result
  
  @staticmethod
  def get_uuid(config = {}):
    result = config.get("uuid")
    if not result:
      raise TypeError('supervisor uuid cannot be empty')
    return result

  @staticmethod
  def get_controllers(config = {}):
    return list(map(ControllerFactory.create_controller, config.get("controllers", [])))
  
  @staticmethod
  def get_interval_seconds(config = {}):
    return config.get("intervalSeconds", 60)
  
  def start(self):
    self._init_resources()
    for controller in self.controllers:
      try:
        controller.subscribe(self._on_controller_value)
        controller.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def exit(self):
    for controller in self.controllers:
      try:
        controller.exit()
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
  def _on_controller_value(self, value, type, uuid):
    pass