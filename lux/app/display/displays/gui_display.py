from lux.app.coord_space import IndexCoordSpace
from lux.core2.color import ColorVector
from lux.core2.main import Display
from lux.core2.pixel import Pixel

from ..integrations.gui import DEFAULT_PIXEL_SIZE, PixelRowGui


class PixelGuiDisplay(Display):

  def __init__(self, pixelsPerRow: int, rows=1) -> None:
    super().__init__()
    self.__numPixels = pixelsPerRow*rows
    self.gui = PixelRowGui(DEFAULT_PIXEL_SIZE, pixelsPerRow, rows)
    self.coordSpace = IndexCoordSpace(self.length)

  def setPixel(self, index: int, color: ColorVector):
    self.gui.setPixel(index, Pixel(color))
  
  def render(self):
    self.gui.window.update()

  @property
  def length(self) -> int:
    return self.__numPixels