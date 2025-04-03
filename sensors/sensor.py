class Sensor:
  def __init__(self, farm_name, crops_name, section_name, config):
    self.farm_name = farm_name
    self.crops_name = crops_name
    self.section_name = section_name
    self.name = Sensor.__get_name(config)
    self.target = Sensor.__get_target(config)
    self.config = Sensor.__get_config(config)

  def run(self):
    print(self.name)
    print(self.target)

  def rerun(self):
    pass

  def exit(self):
    pass

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