from ncf_subscriber import NcfSubscriber

WS_URL = "ws://192.168.30.128:8081/ws"

def _on_message(subscriber, frame):
  print(frame.body)

def _on_subscribe_success(subscriber, frame):
  print('success to subscribe!')

def _on_open(subscriber):
  subscriber.subscribe()

def _on_close(subscriber, close_status_code, close_msg):
  print("socket closed")
  print(close_status_code)
  print(close_msg)

def _on_error(subscriber, error):
  print("socket error")
  print(error)

subscriber = NcfSubscriber(WS_URL, 'test-subject')
subscriber.on_open = _on_open
subscriber.on_close = _on_close
subscriber.on_error = _on_error
subscriber.on_message = _on_message
subscriber.on_subscribe_success = _on_subscribe_success
subscriber.run()