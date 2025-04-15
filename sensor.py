from abc import ABC, abstractmethod

class Sensor(ABC):
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
  def read(self) -> dict:
    pass

  @abstractmethod
  def read_datas(self):
    pass

  @staticmethod
  def get_type(config = {}):
    result = config.get("type", None)
    if result is None:
      raise TypeError("sensor type cannot be empty")
    return result
  
  @staticmethod
  def get_uuid(config = {}):
    result = config.get("uuid")
    if not result:
      raise TypeError("sensor uuid cannot be empty")
    return result