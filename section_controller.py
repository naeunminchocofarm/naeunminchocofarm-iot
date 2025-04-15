from controller import Controller

class SectionController(Controller):
  def __init__(self, type, uuid, sensors=[], actuators=[]):
    super().__init__(type, uuid, sensors, actuators)
    self.sensors_status = {}
    self.actuators_status = {}
  
  @staticmethod
  def from_config(config):
    type = Controller.get_type(config)
    uuid = Controller.get_uuid(config)
    sensors = Controller.get_sensors(config)
    actuators = Controller.get_actuators(config)
    return SectionController(type, uuid, sensors, actuators)
  
  def start(self):
    self._start_sensors()
    self._start_actuators()

  def _start_sensors(self):
    for sensor in self.sensors.values():
      try:
        sensor.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def _start_actuators(self):
    for actuator in self.actuators.values():
      try:
        actuator.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def exit(self):
    self._exit_actuators()
    self._exit_sensors()
  
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
  
  def read(self):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "sensors": [x for x in self._get_sensors_status().values()],
      "actuators": [x for x in self._get_actuators_status().values()]
    }
  
  def _get_sensors_status(self):
    if self.sensors_status == {}:
      self.sensors_status = self._read_sensors_status()
    return self.sensors_status
  
  def _read_sensors_status(self):
    result = {}
    for sensor in self.sensors.values():
      try:
        result[sensor.type] = sensor.read()
      except:
        pass
    return result
  
  def _get_actuators_status(self):
    if self.actuators_status == {}:
      self.actuators_status = self._read_actuators_status()
    return self.actuators_status
  
  def _read_actuators_status(self):
    result = {}
    for actuator in self.actuators.values():
      try:
        result[actuator.type] = actuator.read()
      except:
        pass
    return result
  
  def control(self):
    for sensor in self.sensors.values():
      try:
        sensor_status = sensor.read()
        self.sensors_status[sensor.type] = sensor_status
        match sensor.type:
          case 'air_temp_humid':
            self._control_air_temp(sensor_status)
      except:
        print('An error occurred during control {}'.format(self.uuid))
    self.actuators_status = self._read_actuators_status()

  def _control_air_temp(self, sensor_status):
    air_temp_settings = self.settings.get('air_temp', {})
    enable_air_temp = air_temp_settings.get('enable')
    led = self.actuators.get('led')
    if led is None:
      return
    if enable_air_temp is None or not enable_air_temp:
      led.command('off')
      return
    air_temp = sensor_status.get('air_temp')
    if air_temp is None:
      return
    min_air_temp = air_temp_settings.get('min')
    if min_air_temp is None:
      return
    max_air_temp = air_temp_settings.get('max')
    if max_air_temp is None:
      return
    if air_temp <= min_air_temp:
      led.command('off')
    elif max_air_temp <= air_temp:
      led.command('on')