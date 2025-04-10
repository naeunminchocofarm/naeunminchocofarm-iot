from actuator import Actuator

class LedActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.power = False

  def _init_resources(self):
    pass
  
  def _command(self, action, parameters=[]):
    match action:
      case "on":
        self.power = True
        print('led on!')
      case "off":
        self.power = False
        print('led off.')
  
  def _cleanup_resources(self):
    pass

  def read(self):
    return {
      "type": self.type,
      "uuid": self.uuid,
      "power": self.power
    }
  
  @staticmethod
  def from_config(config: dict):
    type = Actuator.get_type(config)
    uuid = Actuator.get_uuid(config)
    gpio = LedActuator._get_gpio(config)
    return LedActuator(type, uuid, gpio)

  @staticmethod
  def _get_gpio(config = {}):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError('led actuator gpio cannot be empty')
    return result