from actuator import Actuator

class LedActuator(Actuator):
  def __init__(self, gpio):
    super().__init__()
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
    gpio = LedActuator._get_gpio(config)
    return LedActuator(gpio)

  @staticmethod
  def _get_gpio(config = {}):
    result = config.get("gpio", None)
    if result is None:
      raise TypeError('led actuator gpio cannot be empty')
    return result
  

config = {
  "gpio": 17
}

a = LedActuator.from_config(config)

a.start()

a.exit()