from abc import ABC, abstractmethod, abstractproperty
from pixlr.pixel import AnyColor
from typing import Type

class IPixelList(ABC):

  @property
  @abstractproperty
  def numPixels(self) -> int:
    pass

  @abstractmethod
  def setPixel(self, index:int, color:AnyColor):
    pass

  @abstractmethod
  def show(self):
    pass

class PixelStripWriter():
  
  def __init__(self, strip: IPixelList) -> None:
    self.strip = strip

  def setPixels(self, color: AnyColor):
    for i in range(0,self.strip.numPixels):
      self.strip.setPixel(i, color)

  def fill(self, color):
    self.setPixels(color)
    self.strip.show()