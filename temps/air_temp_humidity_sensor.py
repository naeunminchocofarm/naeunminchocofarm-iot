import time
from sensor import Sensor
import board
import adafruit_dht

class AirTempHumiditySensor(Sensor):
  def __init__(self, gpio, interval_seconds=1):
    super().__init__(interval_seconds)
    self.gpio = gpio

  def _init_resources(self):
    self.dhtDevice = self._createDhtDevice()
  
  def _read(self):
    for i in range(10):
      try:
        temperature_c = self.dhtDevice.temperature
        humidity_percentage = self.dhtDevice.humidity
        print("Temp: {:.1f} C    Humidity: {:.1f}% ".format(temperature_c, humidity_percentage))

        return {
          "air_temp": temperature_c,
          "humidity": humidity_percentage
        }
      except RuntimeError as e:
        print(type(e))
        print(e)
      except TypeError as e:
        print(type(e))
        print(e)
    
    return {"air_temp": 0.0, "humidity": 0.0}
  
  def _cleanup_resources(self):
    self.dhtDevice.exit()

  def _createDhtDevice(self):
    pin_key = 'D{}'.format(self.gpio)
    pin = getattr(board, pin_key)
    return adafruit_dht.DHT22(pin)

  @staticmethod
  def from_config(config):
    gpio = AirTempHumiditySensor._get_gpio(config)
    interval_seconds = Sensor.get_interval_seconds(config)
    return AirTempHumiditySensor(gpio, interval_seconds)
  
  @staticmethod
  def _get_gpio(config):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError("air temp humidity sensor gpio cannot empty")
    return result


s = AirTempHumiditySensor.from_config({
  "intervalSeconds": 1,
  "gpio": 27
})

s.subscribe(lambda v: print("temp: {:.2f}'C humidity: {:.2f}%".format(v.get("temp", 0.0), v.get("humidity", 0.0))))

s.start()

print('waiting...')
time.sleep(6)

s.exit()