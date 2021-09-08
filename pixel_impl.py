# import board
# import adafruit_ws2801

# odata = board.MOSI
# oclock = board.SCLK
# numleds = 160
# bright = 1.0

# ### Example for a Feather M4 driving 25 12mm leds
# def init():
#   return adafruit_ws2801.WS2801(
#     oclock, odata, numleds, brightness=bright, auto_write=False
#   )


from typing import List
from pixlr.strip import IPixelList
from abc import ABC, abstractmethod, abstractproperty
import os 

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
    halfIndex = int(lastIndex/2)
    for i in range(0, halfIndex):
      dispStr += self.makeColor(colors[i])
    dispStr += '\n'
    for i in reversed(range(halfIndex, lastIndex)):
      dispStr += self.makeColor(colors[i])
    return dispStr
  

class ConsoleStrip(IPixelList):

  pixels =[[0,0,0]]

  def __init__(self, numLeds, display:ConsoleDisplay) -> None:
    super().__init__(numLeds)
    self.pixels = [[0,0,0]] * numLeds
    self.display = display

  def setPixel(self, index: int, color):
    self.pixels[index] = color

  def makeColor(self, color:List[int]):
    disp = '['
    for i in range(len(color)):
      if (i != 0):
        disp += ', '
      disp += str(color[i]).rjust(3)
    return disp+']'  
    
  def show(self):    
    self.display.show(self.pixels)


# class LoopedConsoleStrip(IPixelList):

#   pixels =[[0,0,0]]

#   def __init__(self, numLeds) -> None:
#     super().__init__(numLeds)
#     self.pixels = [[0,0,0]] * numLeds

#   def setPixel(self, index: int, color):
#     self.pixels[index] = color


    