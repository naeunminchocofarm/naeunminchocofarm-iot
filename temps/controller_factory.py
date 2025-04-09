from section_controller import SectionController

class ControllerFactory:
  @staticmethod
  def create_controller(config = {}):
    type = config.get("type")
    match type:
      case "section":
        return SectionController.from_config(config)
      case _:
        raise TypeError('Unsupported controller type: {}'.format(type))