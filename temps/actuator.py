from abc import ABC, abstractmethod
import threading

class Actuator(ABC):
  def __init__(self):
    self.is_started = False

  def start(self):
    self._init_resources()
    self.is_started = True

  def apply(self, value):
    if not self.is_started:
      raise RuntimeError("Actuator must be started before applying values")
    threading.Thread(target=self._apply, args=(value,), daemon=True).start()

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
  def _apply(self, value: dict):
    pass