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
  
  def render(self):
    self.display.render()

  def clearDisplays(self):
    for i in range(self.display.length):
      self.display.setPixel(i, [0,0,0])
    self.display.render()

class NotCoordinator(Generic[P]):

  instruction: Instruction[P]
  display: Display[P]

  def __init__(self, display, instruction) -> None:
    super().__init__()
    self.display = display
    self.pixels = []
    self.instruction = instruction

  def setPixels(self, pixels):
    self.pixels = pixels

  def updateDisplay(self):
    for i in range(min(self.display.length, len(self.pixels))):
      self.display.setPixel(i, self.pixels[i])
  
  def render(self):
    self.display.render()

  def calcPixels(self, instant: TimeInstant):
    pixels = []
    for i in range(self.display.length):
      point = self.display.coordSpace.getPoint(i)
      color = self.instruction.getColorAtPoint(point, instant, self.display.coordSpace)
      pixels.append(color)
    return pixels

class DynamicNotCoordinator(Generic[P]):

  instruction: Instruction[P] = None
  display: Display[P]

  def __init__(self, display) -> None:
    super().__init__()
    self.display = display
    self.pixels = []

  def setPixels(self, pixels):
    self.pixels = pixels

  def updateDisplay(self):
    for i in range(min(self.display.length, len(self.pixels))):
      self.display.setPixel(i, self.pixels[i])
  
  def render(self):
    self.display.render()

  def calcPixels(self, instant: TimeInstant):
    pixels = []
    for i in range(self.display.length):
      point = self.display.coordSpace.getPoint(i)
      color = self.instruction.getColorAtPoint(point, instant, self.display.coordSpace)
      pixels.append(color)
    return pixels

  def clearDisplays(self):
    for i in range(self.display.length):
      self.display.setPixel(i, [0,0,0])
    self.display.render()