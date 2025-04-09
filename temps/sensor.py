import threading
import time
from abc import ABC, abstractmethod

class Sensor(ABC):
  def __init__(self, interval_seconds = 1):
    self.subscribers = []
    self.stop_event = threading.Event()
    self.task = None
    self.interval_seconds = interval_seconds

  def subscribe(self, callback):
    self.subscribers.append(callback)

  def _notify(self, value):
    for callback in self.subscribers:
      callback(value)

  def start(self):
    self._init_resources()
    self.stop_event.clear()
    self.task = threading.Thread(target=self._loop)
    self.task.start()

  def _loop(self):
    next_time = time.time()
    while not self.stop_event.is_set():
      now = time.time()
      if next_time <= now:
        value = self._read()
        self._notify(value);
        next_time += self.interval_seconds
      time.sleep(1)

  def exit(self):
    self.stop_event.set()
    self._cleanup_resources()
    if self.task:
      self.task.join()

  @abstractmethod
  def _init_resources(self):
    pass

  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _read(self) -> dict:
    pass

  @staticmethod
  def get_interval_seconds(config):
    return config.get('intervalSeconds', 60)