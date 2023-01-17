from typing import TypeVar

from lux.core2.main import CoordSpace

P = TypeVar("P")

class IndexCoordSpace(CoordSpace[int]):
  def __init__(self, length: int) -> None:
    super().__init__()
    self.length = length

  def getPoint(self, index: int) -> P:
    return index

  @property
  def bounds(self):
    return [0, self.length]