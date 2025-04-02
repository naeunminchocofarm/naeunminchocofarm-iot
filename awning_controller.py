import RPi.GPIO as GPIO
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS

led_pin = 4

try:
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(led_pin, GPIO.OUT)

    def _on_open(subs):
        subs.subscribe()
    
    def _on_message(subscriber, frame):
        print(frame.body)
        if frame.body == 'awning-on':
            GPIO.output(led_pin,1)
        elif frame.body == 'awning-off':
            GPIO.output(led_pin,0)
        

    subscriber = NcfSubscriber(WEB_SOCKET_PATHS['production'], DESTINATIONS['awning'])
    subscriber.on_open = _on_open
    subscriber.on_message = _on_message
    subscriber.run_forever()
except:
    print('error!')
finally:
    GPIO.cleanup()
