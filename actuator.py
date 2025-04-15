from abc import ABC, abstractmethod

class Actuator(ABC):
  def __init__(self, type, uuid):
    self.type = type
    self.uuid = uuid

  @abstractmethod
  def start(self):
    pass

  @abstractmethod
  def exit(self):
    pass

  @abstractmethod
  def command(self, action, parameters = {}):
    pass

  @abstractmethod
  def read_datas(self):
    pass

  @staticmethod
  def get_type(config = {}):
    result = config.get("type", None)
    if result is None:
      raise TypeError("actuator type cannot be empty")
    return result
  
  @staticmethod
  def get_uuid(config = {}):
    result = config.get("uuid")
    if not result:
      raise TypeError("actuator uuid cannot be empty")
    return result