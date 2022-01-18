from abc import ABC, abstractmethod, abstractproperty

from .pixel import AnyColor


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

class PixelDisplayWriter():
  
  def __init__(self, display: IPixelList) -> None:
    self.display = display

  def setPixels(self, color: AnyColor):
    for i in range(0,self.display.numPixels):
      self.display.setPixel(i, color)

  def fill(self, color):
    self.setPixels(color)
    self.display.show()
