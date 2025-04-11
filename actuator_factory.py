from led_actuator import LedActuator

class ActuatorFactory:
  @staticmethod
  def create_actuator(config = {}):
    type = config.get("type")
    match type:
      case "led":
        return LedActuator.from_config(config)
      case _:
        raise TypeError('Unsupported actuator type: {}'.format(type))