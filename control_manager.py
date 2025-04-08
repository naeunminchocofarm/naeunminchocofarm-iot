import threading

class ControlManager:
  _instance = None
  _is_initialized = False
  _new_lock = threading.Lock()

  def __new__(cls):
    with cls._new_lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
      return cls._instance

  def __init__(self, config_path = "control_settings.json"):
    with self.__class__._new_lock:
      if self.__class__._is_initialized:
        return
      self.config_path = config_path
      self.config = self._read_config()
      self._lock = threading.Lock()
      self.__class__._is_initialized = True

  def _read_config(self):
    with open(self.config_path, "r") as file:
      import json
      result = json.load(file)
    return result
  
  def _write_config(self):
    with open(self.config_path, "w") as file:
      import json
      json.dump(self.config, file, indent=2)
  
  def get(self, key):
    with self._lock:
      result = self.config.get(key, None)
      return result
  
  def set(self, key, value):
    with self._lock:
      self.config[key] = value
      self._write_config()