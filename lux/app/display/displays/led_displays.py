from math import ceil

from adafruit_ws2801 import WS2801

from lux.app.coord_space import IndexCoordSpace
from lux.core2.color import ColorVector
from lux.core2.main import Display
from lux.core2.pixel import Pixel

class WS2801Display(WS2801, Display[int]):
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)

  def render(self):
    return self.show()

class LinearWS2801Display(WS2801Display):

  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.coordSpace = IndexCoordSpace(len(self))

  def setPixel(self, index: int, color: ColorVector):
    self[index] = Pixel(color)

  @property
  def length(self) -> int:
    return len(self)
    
class MirroredWS2801Display(WS2801Display):
  
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.mirrorOffset = len(self) % 2 + 1
    self.coordSpace = IndexCoordSpace(self.length)

  def setPixel(self, index: int, color: ColorVector):
    self[index] = Pixel(color)
    mirrorIndex = (self.length*2)-index - self.mirrorOffset
    self[mirrorIndex] = Pixel(color)

  @property
  def length(self):
    return ceil(len(self)/2)


  
