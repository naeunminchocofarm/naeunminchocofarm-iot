import threading
import websocket
import time
import json
from ncf_frame import NcfFrame
import inspect
import asyncio

MIN_RECONNECT_DELAY = 1
MAX_RECONNECT_DELAY = 60

class NcfSocketClient:
  def __init__(self, path):
    self.path = path
    self.reconnect_delay = MIN_RECONNECT_DELAY
    self.socket = None
    self.on_text = lambda client, frame: None
    self.on_json = lambda client, frame: None
    self.on_open = lambda client: None
    self.on_close = lambda client, status, msg: None
    self.on_handshake_success = lambda client, frame: None
    self.on_handshake_failed = lambda frame: None
    self.access_token_provider = lambda: ''
    self._is_exit = False

  def connect(self):
    threading.Thread(target=self.run_forever, daemon=True).start()

  def send_frame(self, frame):
    if self.socket and self.socket.sock and self.socket.sock.connected:
      self.socket.send(str(frame))
  
  def _handshake(self):
    def _handshake_task():
      access_token = self.access_token_provider()
      if inspect.isawaitable(access_token):
        loop = asyncio.new_event_loop()
        try:
          asyncio.set_event_loop(loop)
          access_token = loop.run_until_complete(access_token)
        finally:
          loop.close()
      headers = {
        'Authorization': 'Bearer {}'.format(access_token)
      }
      frame = NcfFrame('AUTHENTICATE', headers=headers)
      self.send_frame(frame)
    threading.Thread(target=_handshake_task, daemon=True).start()

  def run_forever(self):
    print('trying to connect websocket')
    self.socket = websocket.WebSocketApp(self.path)
    def on_open(ws):
      self.reconnect_delay = MIN_RECONNECT_DELAY
      print('websocket is opened')
      self.on_open(self)
      self._handshake()
    def on_message(ws, message):
      frame = NcfFrame.parse(message)
      match frame.command:
        case 'AUTH_SUCCESS':
          print("handshake success")
          self.on_handshake_success(self, frame)
        case 'AUTH_FAIL':
          self.close()
          print('handshake failed')
          self.on_handshake_failed(frame)
        case 'MESSAGE':
          match frame.headers.get('content-type'):
            case 'text':
              self.on_text(self, frame)
            case 'json':
              self.on_json(self, frame)
    def on_close(ws, status, msg):
      print('websocket is closed')
      self.on_close(self, status, msg)
      def rerun_forever():
        print(f'reconnect after {self.reconnect_delay} seconds...')
        time.sleep(self.reconnect_delay)
        self.reconnect_delay = min(self.reconnect_delay * 2, MAX_RECONNECT_DELAY)
        self.run_forever()
      if not self._is_exit:
        rerun_forever()

    self.socket.on_open = on_open
    self.socket.on_message = on_message
    self.socket.on_close = on_close
    self._is_exit = False
    self.socket.run_forever()

  def close(self):
    if self.socket and self.socket.sock and self.socket.sock.connected:
      self._is_exit = True
      self.socket.sock.close()
      self.socket = None
  
  def subscribe(self, destination):
    frame = NcfFrame.createSubscribe(destination)
    self.send_frame(frame)

  def unsubscribe(self, destination):
    frame = NcfFrame.createUnsubscribe(destination)
    self.send_frame(frame)

  def send_text(self, destination, text):
    headers = {
      'destination': destination,
      'content-type': 'text'
    }
    frame = NcfFrame.createSend(headers, text)
    self.send_frame(frame)

  def send_json(self, destination, dict):
    headers = {
      'destination': destination,
      'content-type': 'json'
    }
    frame = NcfFrame.createSend(headers, json.dumps(dict))
    self.send_frame(frame)