from pixlr.pixel import AnyColor, Pixel
from pixlr.strip import IPixelList
from adafruit_ws2801 import WS2801
from math import ceil

class WS2801Strip(WS2801, IPixelList):

  def setPixel(self, index: int, color: AnyColor):
    self[index] = Pixel(color)
  
  @property
  def numPixels(self) -> int:
    return len(self)
    
class MirroredWS2801Strip(WS2801, IPixelList):
  
  def __init__(self, *args, **kwargs) -> None:
    super().__init__(*args, **kwargs)
    self.mirrorOffset = len(self) % 2 + 1
  
  def setPixel(self, index: int, color: AnyColor):
    self[index] = Pixel(color)
    mirrorIndex = (self.numPixels*2)-index - self.mirrorOffset
    self[mirrorIndex] = Pixel(color)

  @property
  def numPixels(self):
    return ceil(len(self)/2)


  
