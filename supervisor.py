from controller_factory import ControllerFactory
from abc import ABC, abstractmethod
import json
from settings import Settings

class Supervisor(ABC):
  def __init__(self, type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds):
    self.type = type
    self.uuid = uuid
    self.controllers = controllers
    self.settings_path = settings_path
    self.settings = Supervisor.read_settings(settings_path)
    self.interval_seconds = interval_seconds
    self.realtime_interval_seconds = realtime_interval_seconds
    for controller in self.controllers:
      controller.update_settings(self.settings)

  @abstractmethod
  def start(self):
    pass

  @abstractmethod
  def exit(self):
    pass

  @abstractmethod
  def read(self):
    pass

  @abstractmethod
  def read_sensor_datas(self):
    pass

  def update_settings(self, settings):
    Settings.save(self.settings_path, settings)
    self.settings = Settings.load(self.settings_path)
    for controller in self.controllers:
      controller.update_settings(self.settings)
  
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
  def get_controllers(config):
    return [ControllerFactory.create_controller(x) for x in config.get("controllers", [])]
  
  @staticmethod
  def get_interval_seconds(config = {}):
    return config.get("intervalSeconds", 60)
  
  @staticmethod
  def get_realtime_interval_seconds(config = {}):
    return config.get("realtimeIntervalSeconds", 5)
  
  @staticmethod
  def get_settings_path(config = {}):
    result = config.get("settingsPath")
    if not result:
      raise TypeError('supervisor settings path cannot be empty')
    return result
  
  @staticmethod
  def read_settings(settings_path):
    with open(settings_path, "r") as file:
      return json.load(file)