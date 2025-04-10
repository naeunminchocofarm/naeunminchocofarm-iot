from section_controller import SectionController

class ControllerFactory:
  @staticmethod
  def create_controller(config, interval_seconds):
    type = config.get("type")
    match type:
      case "section":
        return SectionController.create(config, interval_seconds)
      case _:
        raise TypeError('Unsupported controller type: {}'.format(type))