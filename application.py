from farm_supervisor import FarmSupervisor
import json
import time

class Application:
  def __init__(self, app_config_path = "application.json"):
    self.app_config_path = app_config_path
    self.supervisor = None

  def run(self):
    config = self._read_config(self.app_config_path)
    self.supervisor = FarmSupervisor.from_config(config)
    try:
      self.supervisor.start()
      while True:
        time.sleep(3600)
    except KeyboardInterrupt:
      print('stop application.')
    except Exception as err:
      print(type(err))
      print(err)
    except:
      print('An error occurred while running the supervisor.')
    finally:
      self.supervisor.exit()

  def _read_config(self, config_path):
    with open(config_path, "r") as file:
      return json.load(file)