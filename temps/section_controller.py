from controller import Controller

class SectionController(Controller):
  def __init__(self, type, uuid, sensors=[], actuators=[], interval_seconds = 60):
    super().__init__(type, uuid, sensors, actuators, interval_seconds)
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
    self._control_actuators(value, type, uuid)
    self._save_sensors_status(value, type, uuid)

  def _control_actuators(self, sensor_value, sensor_type, sensor_uuid):
    pass

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
  
  # def _on_sensor_value(self, value, type, uuid):
  #   match type:
  #     case 'air_temp_humid':
  #       led_act = self.actuators['led']
  #       if led_act:
  #         led_act.command('on' if value.get('air_temp', 0.0) >= 25.0 else 'off')