from air_temp_humidity_sensor import AirTempHumiditySensor
from led_actuator import LedActuator
import time

s = AirTempHumiditySensor.from_config({
  "intervalSeconds": 1,
  "gpio": 27
})

a = LedActuator.from_config({
  "gpio": 17
})

s.start()
a.start()
s.subscribe(lambda v: a.apply({"led": v.get("air_temp", 0.0) >= 24.0}))

time.sleep(6)

s.exit()
a.exit()