from actuator import Actuator

class LedActuator(Actuator):
  def __init__(self, type, uuid, gpio):
    super().__init__(type, uuid)
    self.gpio = gpio

  def _init_resources(self):
    pass
  
  def _apply(self, value):
    led = value.get("led", None)
    if led is None:
      return
    print("led on!" if led else "led off.")
  
  def _cleanup_resources(self):
    pass
  
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