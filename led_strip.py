from pixlr.pixel import AnyColor, Pixel
from pixlr.strip import IPixelList
from adafruit_ws2801 import WS2801

class WS2801Strip(WS2801, IPixelList):

  def __init__(self) -> None:
    super().__init__()

  def setPixel(self, index: int, color: AnyColor):
    self[index] = Pixel(color)

  def show(self):
    self.show()
  
  @property
  def numPixels(self) -> int:
    return len(self)
    

  
