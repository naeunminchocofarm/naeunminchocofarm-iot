from controller import Controller
import itertools

class SectionController(Controller):
  def __init__(self, type, uuid, sensors=[], actuators=[]):
    super().__init__(type, uuid, sensors, actuators)
    self.sensor_datas = []
    self.actuator_datas = []
  
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
  
  def read_sensor_datas(self):
    return self.sensor_datas
  
  def read_actuator_datas(self):
    return self.actuator_datas
  
  def get_status(self):
    return {
      'type': self.type,
      'uuid': self.uuid,
      'sensor_datas': self.sensor_datas,
      'actuator_datas': self.actuator_datas
    }
  
  def control(self):
    self.sensor_datas = list(itertools.chain.from_iterable(x.read_datas() for x in self.sensors.values()))
    for data in self.sensor_datas:
      try:
        value = data.get('value')
        match data.get('name'):
          case 'air_temp':
            self._control_air_temp(value)
          case 'ldr':
            self._control_ldr(value)
          case 'motion':
            self._control_motion(value)
          case 'humidity':
            self._control_humidity(value)
      except:
        print('An error occurred during control {}'.format(data.get('name')))
    self.actuator_datas = list(itertools.chain.from_iterable(x.read_datas() for x in self.actuators.values()))

  def _control_air_temp(self, air_temp):
    led = self.actuators.get('cooler_led')
    if led is None:
      return
    if air_temp is None:
      led.command('off')
      return
    air_temp_settings = self.settings.get('air_temp', {})
    enable_air_temp = air_temp_settings.get('enable')
    if enable_air_temp is None or not enable_air_temp:
      led.command('off')
      return
    min_air_temp = air_temp_settings.get('min')
    if min_air_temp is not None and air_temp <= min_air_temp:
      led.command('off')
      return
    max_air_temp = air_temp_settings.get('max')
    if max_air_temp is not None and max_air_temp <= air_temp:
      led.command('on')
      return
    
  def _control_ldr(self, ldr):
    led = self.actuators.get('night_light')
    if led is None:
      return
    if ldr is None:
      led.command('off')
      return
    ldr_settings = self.settings.get('ldr', {})
    enable_ldr = ldr_settings.get('enable')
    if enable_ldr is None or not enable_ldr:
      led.command('off')
      return
    min_ldr = ldr_settings.get('min')
    if min_ldr is not None and ldr <= min_ldr:
      led.command('on')
      return
    max_ldr = ldr_settings.get('max')
    if max_ldr is not None and max_ldr <= ldr:
      led.command('off')
      return
    
  def _control_motion(self, pir):
    buzzer = self.actuators.get('buzzer')
    if buzzer is None:
      return
    if pir is None:
      buzzer.command('off')
      return
    pir_settings = self.settings.get('motion', {})
    enable_pir = pir_settings.get('enable')
    if enable_pir is None or not enable_pir:
      buzzer.command('off')
      return
    if pir == 'detected':
      buzzer.command('on')
    else:
      buzzer.command('off')

  def _control_humidity(self, humidity):
    ventilator = self.actuators.get('ventilator')
    if ventilator is None:
      return
    if humidity is None:
      return
    humidity_settings = self.settings.get('humidity', {})
    enable_humidity = humidity_settings.get('enable')
    if enable_humidity is None or not enable_humidity:
      return
    min_humidity = humidity_settings.get('min')
    if min_humidity is not None and humidity <= min_humidity:
      ventilator.command('off')
      return
    max_humidity = humidity_settings.get('max')
    if max_humidity is not None and max_humidity <= humidity:
      ventilator.command('on')
      return