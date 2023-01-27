
from typing import List
from lux.core2.color import ColorVector
from lux.core2.main import Display


class RenderDeferralFacade(Display):

  def __init__(self, display: Display) -> None:
    super().__init__()
    self.display = display
    self.pixels : List[ColorVector] = [[0,0,0]] * self.display.length

  @property
  def coordSpace(self):
    return self.display.coordSpace

  @property
  def length(self) -> int:
    return len(self.pixels)
  
  def setPixel(self, index: int, color: ColorVector):
    self.pixels[index] = color
  
  def render(self):
    for i, pixel in enumerate(self.pixels):
      self.display.setPixel(i, pixel)
    self.display.render()