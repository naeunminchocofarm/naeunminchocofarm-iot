from controller_factory import ControllerFactory
from abc import ABC, abstractmethod

class Supervisor(ABC):
  def __init__(self, controllers):
    self.controllers = controllers

  @staticmethod
  def get_controllers(config = {}):
    return list(map(ControllerFactory.create_controller, config.get("controllers", [])))
  
  def start(self):
    self._init_resources()
    for controller in self.controllers:
      try:
        controller.subscribe(self._on_controller_value)
        controller.start()
      except TypeError as err:
        print(type(err))
        print(err)

  def exit(self):
    for controller in self.controllers:
      try:
        controller.exit()
      except:
        continue
    self._cleanup_resources()

  @abstractmethod
  def _init_resources(self):
    pass

  @abstractmethod
  def _cleanup_resources(self):
    pass

  @abstractmethod
  def _on_controller_value(self, value, type, uuid):
    pass