from workers.worker import Worker

class Sensor(Worker):
  def __init__(self, config):
    super().__init__()
    self.name = Sensor.__get_name(config)
    self.uuid = Sensor._get_uuid(config)
    self.target = Sensor.__get_target(config)
    self.config = Sensor.__get_config(config)

  @staticmethod
  def __get_name(dict = {}):
    result = dict.get('name', None)
    if result is None:
      raise TypeError('sensor name cannot be empty')
    return result
  
  @staticmethod
  def _get_uuid(config = {}):
    result = config.get('uuid', None)
    if result is None:
      raise TypeError('sensor uuid cannot be empty')
    return result
  
  @staticmethod
  def __get_target(config = {}):
    result = config.get('target', None)
    if result is None:
      raise TypeError('sensor type cannot be empty')
    return result
  
  @staticmethod
  def __get_config(config = {}):
    result = config.get('config', {})
    return result