from supervisor import Supervisor
import time

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
    "actuators": actuators_config
  }
]
supervisor_config = {
  "controllers": controllers_config
}

sv = Supervisor.from_config(supervisor_config)

sv.start()
time.sleep(6)
sv.exit()
