from ncf_socket_client import NcfFrame, NcfSocketClient
from auth_store import get_access_token
import json

class SupervisorSocketManager:
  def __init__(self, web_socket_url, destination):
    self.web_socket_url = web_socket_url
    self.supervisor_uuid = destination
    self.socket_client = None
    self.settings_provider = lambda: None
    self.on_update_settings = lambda settings: None
    self.status_provider = lambda: None

  def send_supervisor_settings(self, settings):
    if self.socket_client is None or settings is None:
      return
    data = {
      'method': 'current-settings',
      'settings': settings
    }
    self.socket_client.send_json(destination=self.supervisor_uuid, dict=data)

  def send_supervisor_status(self, status):
    if self.socket_client is None or status is None:
      return
    data = {
      'method': 'current-status',
      'status': status
    }
    self.socket_client.send_json(destination=self.supervisor_uuid, dict=data)

  def start(self):
    self.socket_client = NcfSocketClient(self.web_socket_url)
    def _on_handshake_success(subs, frame):
      self.socket_client.subscribe(self.supervisor_uuid)

    def _on_json(subs, frame: NcfFrame):
      data = json.loads(frame.body)
      match data.get('method'):
        case 'update-settings':
          self.on_update_settings(data.get('settings'))
        case 'get-settings':
          self.send_supervisor_settings(self.settings_provider())
        case 'get-status':
          self.send_supervisor_status(self.status_provider())

    self.socket_client.on_handshake_success = _on_handshake_success
    self.socket_client.on_json = _on_json
    self.socket_client.access_token_provider = get_access_token
    self.socket_client.connect()

  def exit(self):
    if self.socket_client is not None:
      self.socket_client.unsubscribe(self.supervisor_uuid)
      self.socket_client.close()
      self.socket_client = None