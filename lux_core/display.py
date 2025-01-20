from abc import ABC, abstractmethod

from lux_core.color import Color

class Display(ABC):

  @property
  @abstractmethod
  def length(self) -> int:
    pass

  @abstractmethod
  def setPixel(self, index: int, color: Color):
    pass

  @abstractmethod
  def render(self):
    pass