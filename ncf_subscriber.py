import websocket
from ncf_frame import NcfFrame

class NcfSubscriber:
  def __init__(self, path, destination):
    self.destination = destination
    self.socket = websocket.WebSocketApp(path)
    self.on_message = lambda subscriber, frame: None
    self.on_subscribe_success = lambda subscriber, frame: None
    self.on_subscribe_faild = lambda subscriber, frame: None
    self.on_open = lambda subscriber: None
    self.on_close = lambda subscriber, close_status_code, close_msg: None
    self.on_error = lambda subscriber, error: None

  def run_forever(self):
    self.socket.on_open = lambda _: self.on_open(self)
    self.socket.on_close = lambda _, close_status_code, close_msg: self.on_close(self, close_status_code, close_msg)
    self.socket.on_error = lambda _, error: self.on_error(self, error)
    def on_receive(ws, raw_frame):
      frame = NcfFrame.parse(raw_frame)
      match frame.command:
        case 'MESSAGE':
          self.on_message(self, frame)
        case 'SUBSCRIBE_SUCCESS':
          self.on_subscribe_success(self, frame)
        case 'SUBSCRIBE_FAILD':
          self.on_subscribe_faild(self, frame)
    self.socket.on_message = on_receive
    self.socket.run_forever()

  def subscribe(self):
    frame = NcfFrame.createSubscribe(self.destination)
    self.socket.send(str(frame))

  def send(self, headers = {}, body = ''):
    headers['destination'] = self.destination
    frame = NcfFrame.createSend(headers, body)
    self.socket.send(str(frame))