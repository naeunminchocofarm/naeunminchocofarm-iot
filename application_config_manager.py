import threading

class ApplicationConfigManager:
  _instance = None
  _is_initialized = False
  _new_lock = threading.Lock()
  _init_lock = threading.Lock()

  def __new__(cls):
    with cls._new_lock:
      if cls._instance is None:
        cls._instance = super().__new__(cls)
      return cls._instance
    
  def __init__(self, config_path = "application.json"):
    with self.__class__._init_lock:
      if self.__class__._is_initialized:
        return
      self.config_path = config_path
      self.config = ApplicationConfigManager._read_config(config_path)
      self.websocket_path = ApplicationConfigManager._get_websocket_path(self.config)
      self.__class__._is_initialized = True

  @staticmethod
  def _read_config(config_path):
    with open(config_path, "r") as file:
      import json
      return json.load(file)
    
  def _get_websocket_path(config = {}):
    result = config.get('websocketPath', None)
    if result is None:
      raise TypeError('websocket path cannot be empty')
    return result