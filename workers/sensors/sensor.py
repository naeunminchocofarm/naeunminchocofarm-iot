from workers.worker import Worker

class Sensor(Worker):
  def __init__(self, uuid, crops_name, section_name, config):
    super().__init__()
    self.uuid = uuid
    self.crops_name = crops_name
    self.section_name = section_name
    self.name = Sensor.__get_name(config)
    self.target = Sensor.__get_target(config)
    self.config = Sensor.__get_config(config)

  @staticmethod
  def __get_name(dict = {}):
    result = dict.get('name', None)
    if result is None:
      raise TypeError('sensor name cannot be empty')
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
  
  def get_position(self):
    position = {
      'farm-uuid': self.uuid,
      'crops-name': self.crops_name,
      'section-name': self.section_name,
      'sensor-name': self.name
    }
    return position