from tkinter import Canvas, Tk
from typing import List

from lux.core2.pixel import Pixel

DEFAULT_PIXEL_SIZE = 20
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