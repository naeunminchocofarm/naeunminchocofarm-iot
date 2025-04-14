import websocket
from ncf_frame import NcfFrame
import threading
import time
import json

MIN_RECONNECT_DELAY = 1
MAX_RECONNECT_DELAY = 30

def _send(socket, message):
    if socket and socket.sock and socket.sock.connected:
        try:
            socket.send(message)
        except Exception as e:
            print(f'faild message: {message}')

class NcfSubscriber:
    def __init__(self, path, destination):
        self.reconnect_delay = MIN_RECONNECT_DELAY
        self.path = path
        self.destination = destination
        self.socket = None
        self.on_message = lambda subscriber, frame: None
        self.on_subscribe_success = lambda subscriber, frame: None
        self.on_subscribe_faild = lambda subscriber, frame: None
        self.on_open = lambda subscriber: None
        self.on_close = lambda subscriber, close_status_code, close_msg: None
        self.on_error = lambda subscriber, error: None
        self._is_closed = False

    def connect(self):
        threading.Thread(target=self.run_forever, daemon=True).start()
        
    def run_forever(self):
        print('trying to connect websocket')
        self.socket = websocket.WebSocketApp(self.path)

        def on_open(ws):
            print('websocket is open')
            self.reconnect_delay = MIN_RECONNECT_DELAY
            self.on_open(self);
        
        def on_close(ws, status, msg):
            print('websocket is closed')
            self.on_close(self, status, msg)

            def rerun_forever():
                print(f'reconnect after {self.reconnect_delay} seconds...')
                time.sleep(self.reconnect_delay)
                self.reconnect_delay = min(self.reconnect_delay * 2, MAX_RECONNECT_DELAY)
                self.run_forever()

            if not self._is_closed:
                rerun_forever()

        def on_receive(ws, raw_frame):
            frame = NcfFrame.parse(raw_frame)
            match frame.command:
                case 'MESSAGE':
                    self.on_message(self, frame)
                case 'SUBSCRIBE_SUCCESS':
                    self.on_subscribe_success(self, frame)
                case 'SUBSCRIBE_FAILD':
                    self.on_subscribe_faild(self, frame)

        self.socket.on_open = on_open
        self.socket.on_close = on_close
        self.socket.on_error = lambda _, error: self.on_error(self, error)
        self.socket.on_message = on_receive
        
        self.socket.run_forever()
    
    def close(self):
        if self.socket and self.socket.sock and self.socket.sock.connected:
            self._is_closed = True
            self.socket.sock.close()

    def subscribe(self):
        frame = NcfFrame.createSubscribe(self.destination)
        _send(self.socket, str(frame))
    
    def unsubscribe(self):
        frame = NcfFrame.createUnsubscribe(self.destination)
        _send(self.socket, str(frame))

    def send(self, headers = {}, body = ''):
        headers['destination'] = self.destination
        frame = NcfFrame.createSend(headers, body)
        _send(self.socket, str(frame))

    def send_json(self, headers = {}, dict = {}):
        headers['destination'] = self.destination
        headers['content-type'] = 'json'
        frame = NcfFrame.createSend(headers, json.dumps(dict))
        _send(self.socket, str(frame))
