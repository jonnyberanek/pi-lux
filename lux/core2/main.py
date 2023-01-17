from dataclasses import dataclass
import time
from abc import ABC, abstractmethod
from math import floor
from typing import Generic, Tuple, TypeVar

ColorVector = Tuple[int, int, int]

@dataclass
class TimeInstant:
  time: float
  pass

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

class SimpleCoordinator(Coordinator, Generic[P]):

  instruction: Instruction[P] = None

  def __init__(self, display) -> None:
    super().__init__()
    self.display = display

  def updateDisplays(self, instant: TimeInstant):
    for i in range(self.display.length):
      point = self.display.coordSpace.getPoint(i)
      color = self.instruction.getColorAtPoint(point, instant, self.display.coordSpace)
      self.display.setPixel(i, color)
    self.display.render()

class IndexCoordSpace(CoordSpace[int]):
  def __init__(self, length: int) -> None:
    super().__init__()
    self.length = length

  def getPoint(self, index: int) -> P:
    return index

  @property
  def bounds(self):
    return [0, self.length]
  
class IndexArrayDisplay(Display[int]):

  def __init__(self, length: int) -> None:
    super().__init__()
    self.coordSpace = IndexCoordSpace(length)
    self.colors = [tuple((0,0,0)) for _ in range(length)]
  
  @property
  def length(self):
    return len(self.colors)

  def setPixel(self, index: int, color: ColorVector):
    self.colors[index] = color

  def render(self):
    print([("_" if (c[0] < 128) else "X") for c in self.colors])
    

class ChaserInstruction(Instruction[int]):
  def getColorAtPoint(self, point: int, instant: TimeInstant, coordSpace: CoordSpace[int]) -> ColorVector:
    bound = coordSpace.bounds[1]
    value = floor(((instant.time*100 % bound) + point) % bound / bound * 255)
    return [value, value, value]


if __name__ == "__main__":
  print("running test")
  coordinator = SimpleCoordinator(IndexArrayDisplay(15))
  coordinator.instruction = ChaserInstruction()

  # This is the "Animator"
  for i in range(10):
    coordinator.updateDisplays(TimeInstant(time.time()))
    time.sleep(0.01)
 