import time
from farm_supervisor import FarmSupervisor

sensors_config = [
  {
    "type": "air_temp_humid",
    "uuid": "test-sensor-uuid-1",
    "gpio": 27
  },
  {
    "type": "adc",
    "uuid": "test-sensor-uuid-2",
    "ldrChannel": 0,
    "soilMoistureChannel": 1
  }
]
actuators_config = [
  {
    "type": "led",
    "uuid": "test-uuid-2",
    "gpio": 4
  }
]
controllers_config = [
  {
    "type": "section",
    "uuid": "test-controller-uuid-1",
    "sensors": sensors_config,
    "actuators": actuators_config,
  }
]
supervisor_config = {
  "type": "farm",
  "uuid": "test-farm-uuid-1",
  "intervalSeconds": 1,
  "settingsPath": "settings.json",
  "websocketPath": "ws://192.168.30.128:8080/ws",
  "controllers": controllers_config
}

sv = FarmSupervisor.from_config(supervisor_config)
try:
  sv.start()
  time.sleep(10)
  print(sv.read())
except Exception as error:
  print(type(error))
  print(error)
finally:
  sv.exit()
