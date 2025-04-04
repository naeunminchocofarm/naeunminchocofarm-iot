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
    self.crops  = Application._create_crops(config)

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
  def _create_crops(farm_name, config = {}):
    result = config.get(KEY_CROPS, [])
    result = map(lambda x: Crop(farm_name, x), result)
    result = list(result)
    return result

class Crop:
  def __init__(self, farm_name, config):
    self.farm_name = farm_name
    self.name = Crop._get_name(config)
    self.sections = Crop._create_sections(farm_name, self.name, config)

  def run(self):
    _run_children(self.sections)

  def rerun(self):
    pass

  def exit(self):
    _exit_children(self.sections)
  
  @staticmethod
  def _get_name(dict = {}):
    result = dict.get(KEY_NAME, None)
    if result is None:
      raise TypeError('crop name cannot be empty.')
    return result
  
  @staticmethod
  def _create_sections(farm_name, crops_name, config = {}):
    result = config.get(KEY_SECTIONS, [])
    result = map(lambda x: Section(farm_name, crops_name, x), result)
    result = list(result)
    return result
  
from workers.sensors.sensor_factory import SensorFactory
import threading
import time

class Section:
  def __init__(self, farm_name, crops_name, config):
    self.farm_name = farm_name
    self.crops_name = crops_name
    self.name = Section.__get_name(config)
    self.sensors = Section._create_sensors(farm_name, crops_name, self.name, config)
    self.stop_event = threading.Event()

  def run(self):
    def _handle_sensor(sensor):
      try:
        sensor.start()
        while not self.stop_event.is_set():
            sensor.loop()
            time.sleep(1)
      except Exception as err:
        print('error:', err)
      except:
        pass
      finally:
        sensor.exit()

    threads = map(lambda s: threading.Thread(target=lambda: _handle_sensor(s)), self.sensors)
    threads = list(threads)
    self.threads = threads
    for thread in threads:
      thread.start()
    # _run_children(self.sensors)

  def rerun(self):
    pass
  
  def exit(self):
    self.stop_event.set()
    for thread in self.threads:
      thread.join()
    # _exit_children(self.sensors)

  @staticmethod
  def __get_name(dict = {}):
    result = dict.get(KEY_NAME, None)
    if result is None:
      raise TypeError('section name cannot be empty.')
    return result
  
  @staticmethod
  def _create_sensors(farm_name, crops_name, section_name, config = {}):
    result = config.get(KEY_SENSORS, [])
    result = map(lambda x: SensorFactory.create_from_config(farm_name, crops_name, section_name, x), result)
    result = list(result)
    return result