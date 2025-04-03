KEY_NAME = 'name'
KEY_CROPS = 'crops'
KEY_SECTIONS = 'sections'
KEY_SENSORS = 'sensors'
KEY_TYPE = 'type'

def _run_children(children = []):
  for child in children:
    try:
      child.run()
    except:
      try:
        child.rerun()
      except:
        continue

def _exit_children(children = []):
  for child in children:
    try:
      child.exit()
    except:
      continue

class Application:
  def __init__(self):
    config = Application.__read_config()
    self.name = Application.__get_name(config)
    self.crops  = Application.__get_crops(config)

  def run(self):
    _run_children(self.crops)

  def rerun(self):
    pass

  def exit(self):
    _exit_children(self.crops)

  @staticmethod
  def __read_config():
    with open("application.json", "r") as file:
      import json
      result = json.load(file)
    return result

  @staticmethod
  def __get_name(config = {}):
    result =  config.get(KEY_NAME, None)
    if result is None:
      raise TypeError('application name cannot be empty.')
    return result
    
  @staticmethod
  def __get_crops(config = {}):
    result = config.get(KEY_CROPS, [])
    result = map(lambda x: Crop(x), result)
    result = list(result)
    return result

class Crop:
  def __init__(self, dict):
    self.name = Crop.__get_name(dict)
    self.sections = Crop.__get_sections(dict)

  def run(self):
    _run_children(self.sections)

  def rerun(self):
    pass

  def exit(self):
    _exit_children(self.sections)
  
  @staticmethod
  def __get_name(dict = {}):
    result = dict.get(KEY_NAME, None)
    if result is None:
      raise TypeError('crop name cannot be empty.')
    return result
  
  @staticmethod
  def __get_sections(dict = {}):
    result = dict.get(KEY_SECTIONS, [])
    result = map(lambda x: Section(x), result)
    result = list(result)
    return result

from sensors.sensor_factory import SensorFactory

class Section:
  def __init__(self, dict):
    self.name = Section.__get_name(dict)
    self.sensors = Section.__get_sensors(dict)

  def run(self):
    _run_children(self.sensors)

  def rerun(self):
    pass
  
  def exit(self):
    _exit_children(self.sensors)

  @staticmethod
  def __get_name(dict = {}):
    result = dict.get(KEY_NAME, None)
    if result is None:
      raise TypeError('section name cannot be empty.')
    return result
  
  @staticmethod
  def __get_sensors(dict = {}):
    result = dict.get(KEY_SENSORS, [])
    result = map(SensorFactory.create_from_config, result)
    result = list(result)
    return result