from actuator import Actuator

class LedActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio
    self.power = 'off'
    self.is_started = False

  def start(self):
    self.is_started = True

  def exit(self):
    self.is_started = False

  def command(self, action, parameters=[]):
    if not self.is_started:
      raise RuntimeError("Actuator must be started before command")
    match action:
      case "on":
        self.power = 'on'
        print('led on!')
      case "off":
        self.power = 'off'
        print('led off.')

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