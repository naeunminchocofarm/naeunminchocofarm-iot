from air_temp_humidity_sensor import AirTempHumiditySensor
from adc_sensor import AdcSensor

class SensorFactory:
  @staticmethod
  def create_sensor(config = {}):
    type = config.get("type")
    match type:
      case "air_temp_humid":
        return AirTempHumiditySensor.from_config(config)
      case "adc":
        return AdcSensor.from_config(config)
      case _:
        raise TypeError('Unsupported sensor type: {}'.format(type))