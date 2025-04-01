import RPi.GPIO as GPIO
import time
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS
import threading

SENSOR = 17
socket_opened = False

def init_sensor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def create_subscriber():
    def _on_open(subs):
        print('open!')
        socket_opened = True

    def _on_close(subs, status, code):
        socket_opened = False
        
    subscriber = NcfSubscriber(WEB_SOCKET_PATHS['dev'], DESTINATIONS['motion'])
    subscriber.on_open = _on_open
    subscriber.on_close = _on_close
    return subscriber

def send_detect_message(subs):
    subs.send(body='detected')


def run():
    init_sensor()
    subscriber = create_subscriber()
    subscriber.connect()
    print('pir ready...')
    time.sleep(5)
    detected_count = 0
    undetected_count = 0
    try:
        while True:
            time.sleep(1)
            if GPIO.input(SENSOR) == 1:
                send_detect_message(subscriber)
                print(f"Motion Detected({detected_count})")
                undetected_count = 0
                detected_count += 1
            else:
                print(f"undetected({undetected_count})")
                undetected_count += 1
                detected_count = 0
    except KeyboardInterrupt:
        print('Stopped by User')
        GPIO.cleanup()
        
run()
