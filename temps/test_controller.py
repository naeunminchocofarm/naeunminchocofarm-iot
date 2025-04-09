from section_controller import SectionController
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

controller_config = {
  "type": "section",
  "uuid": "test-controller-uuid-1",
  "sensors": sensors_config,
  "actuators": actuators_config,
  "intervalSeconds": 1
}

c = SectionController.from_config(controller_config);
c.start()
time.sleep(6)
c.exit()