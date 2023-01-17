import os
from abc import ABC, abstractmethod, abstractproperty
from math import ceil
from typing import List

from lux.core2.pixel import AnyColor, Pixel
from lux.core.strip import IPixelList

clear = lambda: os.system('cls')

# TODO REMOVE
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


class ConsoleDisplay(ABC):
  def makeColor(self, color:List[int]):
    disp = '['
    for i in range(len(color)):
      if (i != 0):
        disp += ', '
      disp += str(color[i]).rjust(3)
    return disp+']'  

  @staticmethod
  def displayFrame(data: str):
    clear()
    print(data)
    
  @abstractmethod
  def makeFrame(self, colors) -> str:
    pass

  def show(self, colors):
    ConsoleDisplay.displayFrame(self.makeFrame(colors))

class LinearConsoleDisplay(ConsoleDisplay):
  def makeFrame(self, colors) -> str:
    dispStr = ""
    for color in colors:
      dispStr += self.makeColor(color)
    return dispStr

class LoopedConsoleDisplay(ConsoleDisplay):
    
  def makeFrame(self, colors) -> str:
    dispStr = ""
    lastIndex = len(colors)
    halfIndex = ceil(lastIndex/2)
    for i in range(0, halfIndex):
      dispStr += self.makeColor(colors[i])
    dispStr += '\n'
    for i in reversed(range(halfIndex, lastIndex)):
      dispStr += self.makeColor(colors[i])
    return dispStr
  

class ConsoleStrip(IPixelList):

  pixels: List[Pixel]

  def __init__(self, numPixels, display:ConsoleDisplay) -> None:
    super().__init__()
    self.pixels = [Pixel(0,0,0)] * numPixels
    self.display = display

  def setPixel(self, index: int, color:AnyColor):
    self.pixels[index] = Pixel(color)
    
  def show(self):    
    self.display.show(self.pixels)

  @property
  def numPixels(self):
    return len(self.pixels)

class LoopConsiderateConsoleStrip(IPixelList):
  
  pixels: List[Pixel]

  def __init__(self, numPixels) -> None:
    super().__init__()
    self.pixels = [Pixel(0,0,0)] * numPixels
    print(self.pixels[0])
    self.display = LoopedConsoleDisplay()
    self.mirrorOffset = numPixels % 2 + 1

  def setPixel(self, index: int, color: AnyColor):
    self.pixels[index] = Pixel(color)
    mirrorIndex = (self.numPixels*2)-index - self.mirrorOffset
    self.pixels[mirrorIndex] = Pixel(color)
    
  def show(self):    
    self.display.show(self.pixels)
  
  @property
  def numPixels(self):
    return ceil(len(self.pixels)/2)
