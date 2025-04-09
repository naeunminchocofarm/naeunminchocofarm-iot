from supervisor import Supervisor
import threading
import time

class FarmSupervisor(Supervisor):
  def __init__(self, type, uuid, controllers, settings, interval_seconds):
    super().__init__(type, uuid, controllers, settings, interval_seconds)
    self.control_thread = None
    self.stop_control = threading.Event()

  @staticmethod
  def from_config(config = {}):
    type = Supervisor.get_type(config)
    uuid = Supervisor.get_uuid(config)
    controllers = Supervisor.get_controllers(config)
    interval_seconds = Supervisor.get_interval_seconds(config)
    settings_path = Supervisor.get_settings_path(config)
    settings = Supervisor.read_settings(settings_path)
    return FarmSupervisor(type, uuid, controllers, settings, interval_seconds)
      
  def start(self):
    for controller in self.controllers:
      try:
        controller.start()
      except TypeError as err:
        print(type(err))
        print(err)
    self.stop_control.clear()
    self.control_thread = threading.Thread(target=self._handle_control_loop)
    self.control_thread.start()
  
  def exit(self):
    self.stop_control.set()
    for controller in self.controllers:
      try:
        controller.exit()
      except:
        continue
    if self.control_thread:
      self.control_thread.join()
  
  def _handle_control_loop(self):
    next_time = time.time()
    while not self.stop_control.is_set():
      if next_time <= time.time():
        self._control_loop()
        next_time += self.interval_seconds
      time.sleep(0.4)

  def _control_loop(self):
    for controller in self.controllers:
      self._control_air_temp(controller)

      
  # 컨트롤러의 기온, 습도를 비교하여 자동제어
  def _control_air_temp(self, controller):
    controller_status = controller.read()
    ath_status = controller_status['sensors']['air_temp_humid']
    print('Temp: {:.2f}    Humidity: {:.2f}    UUID: {}'.format(ath_status['air_temp'], ath_status['humidity'], ath_status['uuid']))
    led_status = controller_status['actuators']['led']
    min_air_temp = self.settings.get('min_air_temp')
    max_air_temp = self.settings.get('max_air_temp')
    if min_air_temp and led_status['power'] and ath_status['air_temp'] <= min_air_temp:
      controller.command(led_status['type'], 'off')
    elif max_air_temp and not led_status['power'] and max_air_temp <= ath_status['air_temp']:
      controller.command(led_status['type'], 'on')