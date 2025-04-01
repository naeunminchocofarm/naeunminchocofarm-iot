import websocket
from ncf_frame import NcfFrame
import threading

def _send(socket, message):
    if socket and socket.sock and socket.sock.connected:
        try:
            socket.send(message)
        except Exception as e:
            print(f'faild message: {message}')

class NcfSubscriber:
    def __init__(self, path, destination):
        self.path = path
        self.destination = destination
        self.on_message = lambda subscriber, frame: None
        self.on_subscribe_success = lambda subscriber, frame: None
        self.on_subscribe_faild = lambda subscriber, frame: None
        self.on_open = lambda subscriber: None
        self.on_close = lambda subscriber, close_status_code, close_msg: None
        self.on_error = lambda subscriber, error: None

    def connect(self):
        self.socket = websocket.WebSocketApp(self.path)
        self.socket.on_open = lambda _: self.on_open(self)
        def on_close(ws, status, msg):
            self.on_close(self, status, msg)
            self.connect()
        self.socket.on_close = on_close
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
        threading.Thread(target=self.socket.run_forever, daemon=True).start()

    def subscribe(self):
        frame = NcfFrame.createSubscribe(self.destination)
        _send(self.socket, str(frame))

    def send(self, headers = {}, body = ''):
        headers['destination'] = self.destination
        frame = NcfFrame.createSend(headers, body)
        _send(self.socket, str(frame))
