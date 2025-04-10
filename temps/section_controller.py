from controller import Controller
import threading

class SectionController(Controller):
  def __init__(self, type, uuid, sensors=[], actuators=[], interval_seconds = 60):
    super().__init__(type, uuid, sensors, actuators, interval_seconds)

  @staticmethod
  def from_config(config={}):
    type = Controller.get_type(config)
    uuid = Controller.get_uuid(config)
    sensors = Controller.get_sensors(config)
    actuators = Controller.get_actuators(config)
    interval_seconds = Controller.get_interval_seconds(config)
    return SectionController(type, uuid, sensors, actuators, interval_seconds)
  
  def start(self):
    self._start_sensors()
    self._start_actuators()

  def _start_sensors(self):
    for sensor in self.sensors.values():
      try:
        sensor.subscribe(self._handle_sensor_value)
        sensor.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def _handle_sensor_value(self, sensor_status):
    threading.Thread(target=self._automatic_control_actuators, args=(sensor_status,), daemon=True).start()

  def _automatic_control_actuators(self, sensor_status):
    match sensor_status.get('type'):
      case 'air_temp_humid':
        air_temp = sensor_status.get('air_temp')
        min_air_temp = self.settings.get('min_air_temp')
        max_air_temp = self.settings.get('max_air_temp')
        if (air_temp is not None and min_air_temp is not None and max_air_temp is not None):
          self._automatic_control_led(sensor_status['air_temp'], self.settings['min_air_temp'], self.settings['max_air_temp'])

  def _automatic_control_led(self, air_temp, min_air_temp, max_air_temp):
    if 'led' in self.actuators:
      led = self.actuators['led']
      if air_temp <= min_air_temp:
        led.command('off')
      elif max_air_temp <= air_temp:
        led.command('on')

  def _start_actuators(self):
    for actuator in self.actuators.values():
      try:
        actuator.start()
      except TypeError as err:
        print(type(err))
        print(err)
  
  def exit(self):
    self._exit_sensors()
    self._exit_actuators()
  
  def _exit_sensors(self):
    for sensor in self.sensors.values():
      try:
        sensor.exit()
      except:
        continue 
  
  def _exit_actuators(self):
    for actuator in self.actuators.values():
      try:
        actuator.exit()
      except:
        continue

  def command(self, actuator_type, action, parameters=...):
    if actuator_type in self.actuators:
      self.actuators[actuator_type].command(action, parameters)
  
  def read(self):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "sensors": [x.read() for x in self.sensors.values()],
      "actuators": [x.read() for x in self.actuators.values()]
    }