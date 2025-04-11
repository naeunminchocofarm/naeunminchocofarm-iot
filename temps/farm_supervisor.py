from supervisor import Supervisor
from ncf_subscriber import NcfSubscriber, NcfFrame
from ncf_api_server import NcfApiServer, requests
import json
import time
import threading
import datetime
import pytz

class FarmSupervisor(Supervisor):
  def __init__(self, type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds, websocket_path, api_host):
    super().__init__(type, uuid, controllers, settings_path, interval_seconds, realtime_interval_seconds)
    self.websocket_path = websocket_path
    self.subscriber = None
    self.realtime_thread = None
    self.stop_realtime = threading.Event()
    self.api_server = NcfApiServer()
    self.api_host = api_host

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
    self._start_realtime()

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
              self._send_current_settings_to_socket()
            case 'get-settings':
              self._send_current_settings_to_socket()
            case 'get-status':
              self._send_current_status_to_socket(self.read())

    self.subscriber.on_open = _on_open
    self.subscriber.on_message = _on_message
    self.subscriber.connect()

  def _send_current_settings_to_socket(self):
    if self.subscriber is None:
      return
    res = {
      'method': 'current-settings',
      'settings': self.settings
    }
    res = json.dumps(res)
    self.subscriber.send(headers={'content-type': 'json'}, body=res)
  
  def _send_current_status_to_socket(self, status):
    if self.subscriber is None:
      return
    data = json.dumps({
      'method': 'current-status',
      'status': status
    })
    self.subscriber.send(headers={'content-type': 'json'}, body=data)

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
      status = self.read()
      self._send_current_status_to_socket(status)
      if api_time <= time.time():
        self._send_current_status_to_api(status)
        api_time += self.interval_seconds
      time.sleep(max(0, next_time - time.time()))

  def _control_controller(self):
    for controller in self.controllers:
      try:
        controller.control()
      except:
        print('An error occurred while controlling the controller.')

  def _send_current_status_to_api(self, status):
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    datas = []
    sensors_status = [sensor_status for controller_status in status.get('controllers', []) for sensor_status in controller_status.get('sensors', []) ]
    for sensor_status in sensors_status:
      match sensor_status.get('type'):
        case 'air_temp_humid':
          datas.append({
            'name': 'air_temp', 
            'value': sensor_status.get('air_temp', 0.0), 
            'measured-at': measured_at, 
            'sensor-uuid': sensor_status.get('uuid', '')
          })
          datas.append({
            'name': 'humidity', 
            'value': sensor_status.get('humidity', 0.0), 
            'measured-at': measured_at, 
            'sensor-uuid': sensor_status.get('uuid', '')
          })
        case 'adc':
          datas.append({
            'name': 'sunshine', 
            'value': sensor_status.get('ldr', 0), 
            'measured-at': measured_at, 
            'sensor-uuid': sensor_status.get('uuid', '')
          })
          datas.append({
            'name': 'soil_moisture', 
            'value': sensor_status.get('soil_moisture', 0), 
            'measured-at': measured_at, 
            'sensor-uuid': sensor_status.get('uuid', '')
          })
        case 'pir':
          pass
    try:
      self.api_server.send_sensor_datas(datas, self.api_host)
    except requests.exceptions.ConnectionError as err:
      print(type(err))
      print(err)
    except:
      print('An error occurred while requesting the API.')

  def exit(self):
    self._stop_realtime()
    self._stop_socket()
    self._stop_controllers()
  
  def _stop_controllers(self):
    for controller in self.controllers:
      try:
        controller.exit()
      except:
        continue

  def _stop_socket(self):
    if self.subscriber:
      self.subscriber.close()

  def _stop_realtime(self):
    self.stop_realtime.set()
    if self.realtime_thread:
      self.realtime_thread.join()

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
  
  @staticmethod
  def get_api_host(config = {}):
    result = config.get('apiHost')
    if result is None:
      raise TypeError('farm supervisor api host cannot be empty')
    return result