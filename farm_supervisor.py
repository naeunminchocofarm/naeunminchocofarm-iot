from supervisor import Supervisor
from ncf_api_server import NcfApiServer, requests
from supervisor_socket_manager import SupervisorSocketManager
import time
import threading
import itertools

class FarmSupervisor(Supervisor):
  def __init__(self, type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds, websocket_path, api_host):
    super().__init__(type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds)
    self.websocket_path = websocket_path
    self.subscriber = None
    self.realtime_thread = None
    self.stop_realtime = threading.Event()
    self.api_server = NcfApiServer()
    self.api_host = api_host
    self.unsubscribe_controllers_status_methods = []
    self.controllers_status_dict = {}
    self.supervisor_socket_manager = SupervisorSocketManager(websocket_path, self.uuid)

  @staticmethod
  def from_config(config = {}):
    type = Supervisor.get_type(config)
    uuid = Supervisor.get_uuid(config)
    interval_seconds = Supervisor.get_interval_seconds(config)
    realtime_interval_seconds = Supervisor.get_realtime_interval_seconds(config)
    controllers = Supervisor.get_controllers(config)
    settings_path = Supervisor.get_settings_path(config)
    websocket_path = FarmSupervisor.get_websocket_path(config)
    api_host = FarmSupervisor.get_api_host(config)
    return FarmSupervisor(type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds, websocket_path, api_host)
      
  def start(self):
    self._start_controllers()
    self._start_socket()
    self._subscribe_controllers_status()
    self._start_realtime()

  def _subscribe_controllers_status(self):
    self.unsubscribe_controllers_status_methods = [controller.subscribe_status(self._handle_receive_controller_status) for controller in self.controllers]

  def _handle_receive_controller_status(self, controller_status):
    status_copy = controller_status.copy()
    self.controllers_status_dict[status_copy['uuid']] = status_copy
    self.supervisor_socket_manager.send_supervisor_status(self.get_status())

  def _start_controllers(self):
    for controller in self.controllers:
      try:
        controller.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def _start_socket(self):
    self.supervisor_socket_manager.settings_provider = lambda: self.settings
    self.supervisor_socket_manager.status_providor = self.get_status
    def _on_update_settings(settings):
      self.update_settings(settings)
      self.supervisor_socket_manager.send_supervisor_settings(self.settings)
      self._control_controller()
      self.supervisor_socket_manager.send_supervisor_status(self.get_status())
    self.supervisor_socket_manager.on_update_settings = _on_update_settings
    self.supervisor_socket_manager.start()

  def _start_realtime(self):
    self.stop_realtime.clear()
    self.realtime_thread = threading.Thread(target=self._handle_realtime)
    self.realtime_thread.start()

  def _handle_realtime(self):
    time.sleep(5)
    next_time = time.time()
    api_time = time.time()
    while not self.stop_realtime.is_set():
      next_time += self.realtime_interval_seconds
      self._control_controller()
      self.supervisor_socket_manager.send_supervisor_status(self.get_status())
      if api_time <= time.time():
        self._send_current_sensor_datas_to_api()
        api_time += self.interval_seconds
      time.sleep(max(0, next_time - time.time()))

  def _control_controller(self):
    for controller in self.controllers:
        controller.control()

  def _send_current_sensor_datas_to_api(self):
    try:
      self.api_server.send_sensor_datas(self.read_sensor_datas(), self.api_host)
    except requests.exceptions.ConnectionError as err:
      print(type(err))
      print(err)
    except:
      print('An error occurred while requesting the API.')

  def exit(self):
    self._stop_realtime()
    self._unsubscribe_controllers_status()
    self._stop_socket()
    self._stop_controllers()

  def _unsubscribe_controllers_status(self):
    for unsubscribe in self.unsubscribe_controllers_status_methods:
      unsubscribe()
  
  def _stop_controllers(self):
    for controller in self.controllers:
      try:
        controller.exit()
      except:
        continue

  def _stop_socket(self):
    self.supervisor_socket_manager.exit()

  def _stop_realtime(self):
    self.stop_realtime.set()
    if self.realtime_thread:
      self.realtime_thread.join()

  def read_sensor_datas(self):
    return list(itertools.chain.from_iterable(x.read_sensor_datas() for x in self.controllers))
  
  def _create_status(self, controllers_status):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "controllers": controllers_status
    }

  def get_status(self):
    return self._create_status(list(self.controllers_status_dict.values()))

  @staticmethod
  def get_websocket_path(config = {}):
    result = config.get('websocketPath')
    if not result:
      raise TypeError('Farm supervisor websocket path cannot be empty')
    return result
  
  @staticmethod
  def get_api_host(config = {}):
    result = config.get('apiHost')
    if result is None:
      raise TypeError('farm supervisor api host cannot be empty')
    return result