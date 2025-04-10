from sensor import Sensor
import spidev

class AdcSensor(Sensor):
  def __init__(self, type, uuid, ldr_channel, soil_moisture_channel):
    super().__init__(type, uuid)
    self.ldr_channel = ldr_channel
    self.soil_moisture_channel = soil_moisture_channel
    self.spi = None
  
  def start(self):
    self.spi = spidev.SpiDev()
    self.spi.open(0, 0)
    self.spi.max_speed_hz = 100000
  
  def exit(self):
    self.spi.close()
    self.spi = None
  
  def read(self):
    return {
      'type': self.type,
      'uuid': self.uuid,
      'ldr': self._read_ldr_value(),
      'soil_moisture': self._read_soil_moisture()
    }
  
  def _read_ldr_value(self):
    return self._read_channel(self.ldr_channel)
  
  def _read_soil_moisture(self):
    return self._read_channel(self.soil_moisture_channel)
  
  def _read_channel(self, channel):
    if channel is None:
      return None
    if channel > 7 or channel < 0:
      return None
    if self.spi is None:
      return None
    r = self.spi.xfer2([1, (8 + channel) << 4, 0])
    return ((r[1] & 3) << 8) + r[2]
  
  @staticmethod
  def from_config(config):
    type = Sensor.get_type(config)
    uuid = Sensor.get_uuid(config)
    ldr_channel = AdcSensor.get_ldr_channel(config)
    soil_moisture_channel = AdcSensor.get_soil_moisture_channel(config)
    return AdcSensor(type, uuid, ldr_channel, soil_moisture_channel)
  
  @staticmethod
  def get_ldr_channel(config = {}):
    return config.get('ldrChannel')
  
  @staticmethod
  def get_soil_moisture_channel(config = {}):
    return config.get('soilMoistureChannel')