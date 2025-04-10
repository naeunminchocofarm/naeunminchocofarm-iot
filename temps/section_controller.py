from controller import Controller
import threading
import time

class SectionController(Controller):
  def __init__(self, type, uuid, interval_seconds, sensors=[], actuators=[]):
    super().__init__(type, uuid, sensors, actuators)
    self.auto_thread = None
    self.stop_auto = threading.Event()
    self.interval_seconds = interval_seconds
  
  @staticmethod
  def create(config, interval_seconds):
    type = Controller.get_type(config)
    uuid = Controller.get_uuid(config)
    sensors = Controller.get_sensors(config)
    actuators = Controller.get_actuators(config)
    return SectionController(type, uuid, interval_seconds, sensors, actuators)
  
  def start(self):
    self._start_sensors()
    self._start_actuators()
    self._start_auto_control()

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

  def _start_auto_control(self):
    self.stop_auto.clear()
    self.auto_thread = threading.Thread(target=self._handle_auto_control)
    self.auto_thread.start()

  def _handle_auto_control(self):
    next_time = time.time() + 5
    while not self.stop_auto.is_set():
      time.sleep(0.4)
      if time.time() < next_time:
        continue
      for sensor in self.sensors.values():
        try:
          self._control_sensor(sensor)
        except:
          pass

  def _control_sensor(self, sensor):
    match sensor.type:
      case 'air_temp_humid':
        self._control_air_temp(sensor)

  def _control_air_temp(self, sensor):
    led = self.actuators.get('led')
    if led is None:
      return
    status = sensor.read()
    air_temp = status.get('air_temp')
    if air_temp is None:
      return
    min_air_temp = self.settings.get('min_air_temp')
    if min_air_temp is None:
      return
    max_air_temp = self.settings.get('max_air_temp')
    if max_air_temp is None:
      return
    if air_temp <= min_air_temp:
      led.command('off')
    elif max_air_temp <= air_temp:
      led.command('on')

  def exit(self):
    self._exit_sensors()
    self._exit_actuators()
    self._stop_auto_control()
  
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

  def _stop_auto_control(self):
    self.stop_auto.set()
    if self.auto_thread is not None:
      self.auto_thread.join()

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