import RPi.GPIO as GPIO
import time
from ncf_subscriber import NcfSubscriber
from consts import WEB_SOCKET_PATHS, DESTINATIONS

SENSOR = 17

def init_sensor():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

def create_subscriber():
    return NcfSubscriber(WEB_SOCKET_PATHS['production'], DESTINATIONS['motion'])

def send_detect_message(subs):
    subs.send(body='detected')

def run():
    init_sensor()
    subscriber = create_subscriber()
    subscriber.connect()
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
    except:
        print('error!')
    finally:
        GPIO.cleanup()
        
run()