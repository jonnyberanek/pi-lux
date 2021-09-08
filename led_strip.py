from pixlr.pixel import AnyColor, Pixel
from pixlr.strip import IPixelList
from adafruit_ws2801 import WS2801

class WS2801Strip(WS2801, IPixelList):

  def setPixel(self, index: int, color: AnyColor):
    self[index] = Pixel(color)
  
  @property
  def numPixels(self) -> int:
    return len(self)
    

  
