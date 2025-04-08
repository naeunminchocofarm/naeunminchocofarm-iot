from workers.worker import Worker

class Actuator(Worker):
  def __init__(self, config):
    super().__init__()
    self.uuid = self._get_uuid(config)
    self.config = self._get_config(config)

  def _get_uuid(config = {}):
    result = config.get('uuid', None)
    if result is None:
      raise TypeError('actuator uuid cannot be empty')
    return result

  def _get_config(config = {}):
    result = config.get('config', {})
    return result
