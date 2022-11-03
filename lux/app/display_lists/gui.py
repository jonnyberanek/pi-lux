from abc import abstractmethod
import os
from tkinter import Canvas, Tk
from typing import List

from lux.core.pixel import AnyColor, Pixel
from lux.core.strip import IPixelList
import math

clear = lambda: os.system('cls')

PIXEL_SIZE = 20
OUTLINE_OFFSET = 1
BORDER_COLOR = "#222"

class PixelRowGui():

  """
  Class that displays and manages a GUI shows a row of squares, 
  to emulate a strip of LEDs
  """

  pixelSize: int
  pixelsPerRow: int
  rows: int

  pixelRectIds: List[int]
  canvas: Canvas
  window: Tk

  def __pixelRect(self, col: int, row: int):
    return (
      col * self.pixelSize, 
      row*self.pixelSize - OUTLINE_OFFSET, 
      col * self.pixelSize + self.pixelSize, 
      (row+1) * self.pixelSize
    )
  
  def __init__(self, pixelSize: int, pixelsPerRow: int, rows=1):
    self.pixelSize = pixelSize
    self.pixelsPerRow = pixelsPerRow
    self.rows = rows
    self.createDisplay()

  def createDisplay(self):
    canvasWidth = self.pixelSize * self.pixelsPerRow
    canvasHeight = self.pixelSize * self.rows

    self.window = Tk()
    self.window.geometry(f"{canvasWidth}x{canvasHeight}")
    self.window.title("Pixels")

    # Canvas with properties to avoid padding
    self.canvas = Canvas(self.window, width=canvasWidth, height=canvasHeight,
      bd=0, highlightthickness=0, relief='ridge')
    self.canvas.pack()

    self.pixelRectIds = []
    for y in range(self.rows):
      for x in range(self.pixelsPerRow):
        id = self.canvas.create_rectangle(
          *self.__pixelRect(x,y), 
          fill="black",
          outline=BORDER_COLOR
        )
        self.pixelRectIds.append(id)

    self.window.update()

  def setPixel(self, index: int, pixel: Pixel):
    self.canvas.itemconfig(
      self.pixelRectIds[index],
      fill=pixel.toHex()
    )

# def rotate(points, angle, center):
#   angle = math.radians(angle)
#   cos_val = math.cos(angle)
#   sin_val = math.sin(angle)
#   cx, cy = center
#   new_points = []
#   for x_old, y_old in points:
#     x_old -= cx
#     y_old -= cy
#     x_new = x_old * cos_val - y_old * sin_val
#     y_new = x_old * sin_val + y_old * cos_val
#     new_points.append([x_new + cx, y_new + cy])
#   return new_points

# class DisplayMapper(ABC):

#   @abstractmethod
#   def getCoordinate(self, ):
#     pass

class PixelGuiDisplay(IPixelList):

  # mapper: DisplayMapper

  # ppr*rows = t   coord = (int(idx/ppr), idx%rows)  

  def __init__(self, pixelsPerRow: int, rows=1) -> None:
    super().__init__()
    self.__numPixels = pixelsPerRow*rows
    self.gui = PixelRowGui(PIXEL_SIZE, pixelsPerRow, rows)

  def setPixel(self, index: int, color:AnyColor):
    self.gui.setPixel(index, Pixel(color))
    
  def show(self):    
    self.gui.window.update()

  @property
  def numPixels(self):
    return self.__numPixels