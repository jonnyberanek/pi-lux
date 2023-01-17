from abc import ABC, abstractmethod
from typing import Generic, Tuple, TypeVar

from .color import ColorVector
from .timely import TimeInstant

P = TypeVar("P")

class CoordSpace(ABC, Generic[P]):

  @abstractmethod
  def getPoint(self, index: int) -> P:
    pass

  @property
  @abstractmethod
  def bounds(self) -> Tuple[P, P]:
    pass

class Display(ABC, Generic[P]):
  coordSpace: CoordSpace[P]

  @property
  @abstractmethod
  def length(self) -> int:
    pass

  @abstractmethod
  def setPixel(self, index: int, color: ColorVector):
    pass

  @abstractmethod
  def render(self):
    pass

class Instruction(ABC, Generic[P]):

  @abstractmethod
  def getColorAtPoint(self, point: P, instant: TimeInstant, coordSpace: CoordSpace[P]) -> ColorVector:
    pass

class Coordinator(ABC):

  @abstractmethod
  def updateDisplays(self, instant: TimeInstant):
    pass

  @abstractmethod
  def clearDisplays(self):
    pass
