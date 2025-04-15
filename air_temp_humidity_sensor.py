from sensor import Sensor
import board
import adafruit_dht
import datetime
import pytz

class AirTempHumiditySensor(Sensor):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.is_ready = False

  def start(self):
    self.dhtDevice = self._createDhtDevice()
    self.is_ready = True

  def read_datas(self):
    measured_at = datetime.datetime.now().astimezone(pytz.timezone("Asia/Seoul")).isoformat()
    if not self.is_ready:
      return []
    for i in range(5):
      try:
        return [
          {
            "name": "air_temp",
            "value": self.dhtDevice.temperature,
            "measured-at": measured_at,
            "uuid": self.uuid,
            "type": self.type
          },
          {
            "name": "humidity",
            "value": self.dhtDevice.humidity,
            "measured-at": measured_at,
            "uuid": self.uuid,
            "type": self.type
          }
        ]
      except RuntimeError as e:
        print(type(e))
        print(e)
      except TypeError as e:
        print(type(e))
        print(e)
    return []
  
  def exit(self):
    self.is_ready = False
    self.dhtDevice.exit()

  def _createDhtDevice(self):
    pin_key = 'D{}'.format(self.gpio)
    pin = getattr(board, pin_key)
    return adafruit_dht.DHT22(pin)

  @staticmethod
  def from_config(config):
    type = Sensor.get_type(config)
    uuid = Sensor.get_uuid(config)
    gpio = AirTempHumiditySensor._get_gpio(config)
    return AirTempHumiditySensor(type, uuid, gpio)
  
  @staticmethod
  def _get_gpio(config):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError("air temp humidity sensor gpio cannot empty")
    return result