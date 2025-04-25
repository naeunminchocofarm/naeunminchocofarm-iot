from ncf_subscriber import NcfSubscriber, NcfFrame
import json

class SupervisorSocketManager:
  def __init__(self, web_socket_url, destination):
    self.web_socket_url = web_socket_url
    self.supervisor_uuid = destination
    self.subscriber = None
    self.settings_provider = lambda: None
    self.on_update_settings = lambda settings: None
    self.status_providor = lambda: None

  def send_supervisor_settings(self, settings):
    if self.subscriber is None or settings is None:
      return
    res = {
      'method': 'current-settings',
      'settings': settings
    }
    self.subscriber.send_json(dict=res)

  def send_supervisor_status(self, status):
    if self.subscriber is None or status is None:
      return
    data = {
      'method': 'current-status',
      'status': status
    }
    self.subscriber.send_json(dict=data)

  def start(self):
    self.subscriber = NcfSubscriber(self.web_socket_url, self.supervisor_uuid)
    def _on_open(subs):
      self.subscriber.subscribe()

    def _on_json(subs, frame: NcfFrame):
      data = json.loads(frame.body)
      match data.get('method'):
        case 'update-settings':
          self.on_update_settings(data.get('settings'))
        case 'get-settings':
          self.send_supervisor_settings(self.settings_provider())
        case 'get-status':
          self.send_supervisor_status(self.status_providor())

    self.subscriber.on_open = _on_open
    self.subscriber.on_json = _on_json
    self.subscriber.connect()

  def exit(self):
    if self.subscriber is not None:
      self.subscriber.unsubscribe()
      self.subscriber.close()
      self.subscriber = None