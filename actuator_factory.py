from led_actuator import LedActuator
from night_light_actuator import NightLightActuator
from buzzer_actuator import BuzzerActuator
from ventilator_actuator import VentilatorActuator

class ActuatorFactory:
  @staticmethod
  def create_actuator(config = {}):
    type = config.get("type")
    match type:
      case "cooler_led":
        return LedActuator.from_config(config)
      case "night_light":
        return NightLightActuator.from_config(config)
      case "buzzer":
        return BuzzerActuator.from_config(config)
      case "ventilator":
        return VentilatorActuator.from_config(config)
      case _:
        raise TypeError('Unsupported actuator type: {}'.format(type))