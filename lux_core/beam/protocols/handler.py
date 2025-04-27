from abc import ABC, abstractmethod

from websockets import Data, ServerConnection

from lux_core.beam.core import BeamRequest


class ProtocolHandler(ABC):

  def __init__(self) -> None:
    super().__init__()

  @abstractmethod
  def handle_requests(self, requests: list[BeamRequest]) -> Data:
    pass

  @abstractmethod
  def handle_exception(self, exception: Exception) -> Data:
    pass


  # @abstractmethod
  # def is_of_protocol(self, data: Data):
  #   pass