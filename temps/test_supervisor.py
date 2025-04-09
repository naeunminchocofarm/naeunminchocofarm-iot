import time
from farm_supervisor import FarmSupervisor

sensors_config = [
  {
    "type": "air_temp_humid",
    "uuid": "test-uuid-1",
    "intervalSeconds": 1,
    "gpio": 27
  }
]
actuators_config = [
  {
    "type": "led",
    "uuid": "test-uuid-2",
    "gpio": 17
  }
]
controllers_config = [
  {
    "type": "section",
    "uuid": "test-controller-uuid-1",
    "sensors": sensors_config,
    "actuators": actuators_config,
    "intervalSeconds": 1
  }
]
supervisor_config = {
  "type": "farm",
  "uuid": "test-farm-uuid-1",
  "controllers": controllers_config,
  "intervalSeconds": 2,
  "settingsPath": "settings.json"
}


sv = FarmSupervisor.from_config(supervisor_config)
try:
  sv.start()
  time.sleep(10)
except Exception as error:
  print(type(error))
  print(error)
finally:
  sv.exit()
