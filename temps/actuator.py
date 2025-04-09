from abc import ABC, abstractmethod
import threading

class Actuator(ABC):
  def __init__(self, type, uuid):
    self.type = type
    self.uuid = uuid
    self.is_started = False

  def start(self):
    self._init_resources()
    self.is_started = True

  def command(self, action, parameters = {}):
    if not self.is_started:
      raise RuntimeError("Actuator must be started before command")
    threading.Thread(target=self._command, args=(action, parameters), daemon=True).start()

  def exit(self):
    self._cleanup_resources()
    self.is_started = False

  @abstractmethod
  def _init_resources(self):
    pass

  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _command(self, action, parameters = {}):
    pass

  @abstractmethod
  def read(self) -> dict:
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