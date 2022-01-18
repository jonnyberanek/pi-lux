import os
from ledcontroller.pixel import AnyColor, Pixel
from typing import List
from tkinter import Tk, Canvas
from ledcontroller.strip import IPixelList

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
  numPixels: int
  pixelRectIds: List[int]
  canvas: Canvas
  window: Tk

  def __pixelRect(self, index: int):
    return (
      index * self.pixelSize, 
      -OUTLINE_OFFSET, 
      index * self.pixelSize + self.pixelSize, 
      self.pixelSize
    )
  
  def __init__(self, pixelSize: int, numPixels: int):
    self.pixelSize = pixelSize
    self.numPixels = numPixels
    self.createDisplay()

  def createDisplay(self):
    canvasWidth = self.pixelSize * self.numPixels
    canvasHeight = self.pixelSize

    self.window = Tk()
    self.window.geometry(f"{canvasWidth}x{canvasHeight}")
    self.window.title("Pixels")

    # Canvas with properties to avoid padding
    self.canvas = Canvas(self.window, width=canvasWidth, height=canvasHeight,
      bd=0, highlightthickness=0, relief='ridge')
    self.canvas.pack()

    self.pixelRectIds = []
    for i in range(self.numPixels):
      id = self.canvas.create_rectangle(
        *self.__pixelRect(i), 
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

class PixelGuiDisplay(IPixelList):

  def __init__(self, numPixels) -> None:
    super().__init__()
    self.__numPixels = numPixels
    self.gui = PixelRowGui(PIXEL_SIZE, self.__numPixels)

  def setPixel(self, index: int, color:AnyColor):
    self.gui.setPixel(index, Pixel(color))
    
  def show(self):    
    self.gui.window.update()

  @property
  def numPixels(self):
    return self.__numPixels