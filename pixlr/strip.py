from abc import ABC, abstractmethod, abstractproperty
from typing import Type

class IPixelList(ABC):
  
  def __init__(self, numLeds) -> None:
    super().__init__()
    self.numLeds = numLeds

  @abstractmethod
  def setPixel(self, index:int, color):
    pass

  @abstractmethod
  def show(self):
    pass
  


class PixelStripWriter():
  
  def __init__(self, strip: IPixelList) -> None:
    self.strip = strip

  def setPixels(self, color):
    for i in range(0,self.strip.numLeds):
      self.strip.setPixel(i, color)

  def fill(self, color):
    self.setPixels(color)
    self.strip.show()