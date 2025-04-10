from supervisor import Supervisor
from ncf_subscriber import NcfSubscriber, NcfFrame
import json

class FarmSupervisor(Supervisor):
  def __init__(self, type, uuid, controllers, settings, interval_seconds, websocket_path):
    super().__init__(type, uuid, controllers, settings, interval_seconds)
    self.websocket_path = websocket_path
    self.subscriber = None

  @staticmethod
  def from_config(config = {}):
    type = Supervisor.get_type(config)
    uuid = Supervisor.get_uuid(config)
    interval_seconds = Supervisor.get_interval_seconds(config)
    controllers = Supervisor.get_controllers(config, interval_seconds)
    settings_path = Supervisor.get_settings_path(config)
    settings = Supervisor.read_settings(settings_path)
    websocket_path = FarmSupervisor.get_websocket_path(config)
    return FarmSupervisor(type, uuid, controllers, settings, interval_seconds, websocket_path)
      
  def start(self):
    self._start_controllers()
    self._start_socket()

  def _start_controllers(self):
    for controller in self.controllers:
      try:
        controller.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def _start_socket(self):
    self.subscriber = NcfSubscriber(self.websocket_path, self.uuid)
    def _on_open(subs):
      self.subscriber.subscribe()

    def _on_message(subs, frame: NcfFrame):
      match frame.headers.get('content-type'):
        case 'json':
          data = json.loads(frame.body)
          match data.get('method'):
            case 'update-settings':
              settings = data.get('settings', {})
              self.update_settings(settings)
              self._response_socket_current_settings()
            case 'get-settings':
              self._response_socket_current_settings()
            case 'get-status':
              self._response_socket_current_status()

    self.subscriber.on_open = _on_open
    self.subscriber.on_message = _on_message
    self.subscriber.connect()

  def _response_socket_current_settings(self):
    if self.subscriber is None:
      return
    res = {
      'method': 'current-settings',
      'settings': self.settings
    }
    res = json.dumps(res)
    self.subscriber.send(headers={'content-type': 'json'}, body=res)
  
  def _response_socket_current_status(self):
    if self.subscriber is None:
      return
    res = {
      'method': 'current-status',
      'status': self.read()
    }
    res = json.dumps(res)
    self.subscriber.send(headers={'content-type': 'json'}, body=res)

  def exit(self):
    self._stop_controllers()
    self._stop_socket()
  
  def _stop_controllers(self):
    for controller in self.controllers:
      try:
        controller.exit()
      except:
        continue

  def _stop_socket(self):
    if self.subscriber:
      self.subscriber.close()

  def read(self):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "controllers": [x.read() for x in self.controllers]
    }

  @staticmethod
  def get_websocket_path(config = {}):
    result = config.get('websocketPath')
    if not result:
      raise TypeError('Farm supervisor websocket path cannot be empty')
    return result