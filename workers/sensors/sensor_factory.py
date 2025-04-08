from .air_temp_humidity_sensor import AirTemperatureHumiditySensor
from .adc_sensor import AdcSensor
from .pir_sensor import PirSensor

class SensorFactory:
  def __init__(self):
    pass

  @staticmethod
  def create_from_config(config):
    model = SensorFactory._get_model(config)
    match model:
      case "DHT22":
        return AirTemperatureHumiditySensor(config)
      case "ADC": 
        return AdcSensor(config)
      case "PIR":
        return PirSensor(config)
      case _:
        raise TypeError('Unusable model.')
      
  @staticmethod
  def _get_model(config = {}):
    result = config.get('model', None)
    if result is None:
      raise TypeError('model cannot be empty')
    return result