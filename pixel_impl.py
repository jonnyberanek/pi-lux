import os
from abc import ABC, abstractmethod
from typing import List
from math import ceil

from pixlr.strip import IPixelList

clear = lambda: os.system('cls')

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

  pixels =[[0,0,0]]

  def __init__(self, numPixels, display:ConsoleDisplay) -> None:
    super().__init__()
    self.pixels = [[0,0,0]] * numPixels
    self.display = display

  def setPixel(self, index: int, color):
    self.pixels[index] = color
    
  def show(self):    
    self.display.show(self.pixels)

  @property
  def numPixels(self):
    return len(self.pixels)

class LoopConsiderateConsoleStrip(IPixelList):
  
  pixels =[[0,0,0]]

  def __init__(self, numPixels) -> None:
    super().__init__()
    self.pixels = [[0,0,0]] * numPixels
    self.display = LoopedConsoleDisplay()
    self.mirrorOffset = numPixels % 2 + 1

  def setPixel(self, index: int, color):
    self.pixels[index] = color
    mirrorIndex = (self.numPixels*2)-index - self.mirrorOffset
    self.pixels[mirrorIndex] = color
    
  def show(self):    
    self.display.show(self.pixels)
  
  @property
  def numPixels(self):
    return ceil(len(self.pixels)/2)