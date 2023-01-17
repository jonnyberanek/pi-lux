from lux.app.coord_space import IndexCoordSpace
from lux.core2.color import ColorVector
from lux.core2.main import Display


class CliIndexDisplay(Display[int]):

  def __init__(self, length: int) -> None:
    super().__init__()
    self.coordSpace = IndexCoordSpace(length)
    self.colors = [tuple((0,0,0)) for _ in range(length)]
  
  @property
  def length(self):
    return len(self.colors)

  def setPixel(self, index: int, color: ColorVector):
    self.colors[index] = color

  def render(self):
    print([("_" if (c[0] < 128) else "X") for c in self.colors])