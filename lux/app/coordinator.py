from typing import Generic, TypeVar

from lux.core2.main import Coordinator, Display, Instruction
from lux.core2.timely import TimeInstant

P = TypeVar("P")

class SimpleCoordinator(Coordinator, Generic[P]):

  instruction: Instruction[P] = None
  display: Display[P]

  def __init__(self, display) -> None:
    super().__init__()
    self.display = display

  def updateDisplays(self, instant: TimeInstant):
    for i in range(self.display.length):
      point = self.display.coordSpace.getPoint(i)
      color = self.instruction.getColorAtPoint(point, instant, self.display.coordSpace)
      self.display.setPixel(i, color)
    self.display.render()

  def clearDisplays(self):
    for i in range(self.display.length):
      self.display.setPixel(i, [0,0,0])
    self.display.render()