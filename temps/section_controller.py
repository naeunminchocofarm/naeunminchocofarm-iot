from controller import Controller

class SectionController(Controller):
  def __init__(self, type, uuid, settings, sensors=[], actuators=[], interval_seconds = 60):
    super().__init__(type, uuid, settings, sensors, actuators, interval_seconds)
    self.sensors_status = {}

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

  def _handle_sensor_value(self, value, type, uuid):
    self._automatic_control_actuators(value, type)
    self._save_sensors_status(value, type, uuid)

  def _automatic_control_actuators(self, sensor_value, sensor_type):
    match sensor_type:
      case 'air_temp_humid':
        if (
          'air_temp' in sensor_value 
          and 'min_air_tmep' in self.settings 
          and 'max_air_temp' in self.settings
        ):
          self._automatic_control_led(sensor_value['air_temp'], self.settings['min_air_temp'], self.settings['max_air_temp'])

  def _automatic_control_led(self, air_temp, min_air_temp, max_air_temp):
    if 'led' in self.actuators:
      led = self.actuators['led']
      if air_temp <= min_air_temp:
        led.command('off')
      elif max_air_temp <= air_temp:
        led.command('on')

  def _save_sensors_status(self, sensor_value, sensor_type, sensor_uuid):
    sensor_value.update({
      "uuid": sensor_uuid
    })
    self.sensors_status[sensor_type] = sensor_value

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
    actuators_status = {}
    for actuator in self.actuators.values():
      status = actuator.read()
      status.update({
        "uuid": actuator.uuid
      })
      actuators_status[actuator.type] = status
    result = {
      "sensors": self.sensors_status,
      "actuators": actuators_status
    }
    return result