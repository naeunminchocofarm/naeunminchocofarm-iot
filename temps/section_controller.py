from controller import Controller

class SectionController(Controller):
  def __init__(self, type, uuid, sensors=..., actuators=...):
    super().__init__(type, uuid, sensors, actuators)

  @staticmethod
  def from_config(config={}):
    type = Controller.get_type(config)
    uuid = Controller.get_uuid(config)
    sensors = Controller.get_sensors(config)
    actuators = Controller.get_actuators(config)
    return SectionController(type, uuid, sensors, actuators)
  
  def _init_resources(self):
    pass
  
  def _cleanup_resources(self):
    pass
  
  def _on_sensor_value(self, value, type, uuid):
    match type:
      case 'air_temp_humid':
        led_act = self.actuators['led']
        if led_act:
          led_act.apply({'led': value.get('air_temp', 0.0) >= 25.7})