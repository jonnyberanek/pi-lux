from math import floor

from lux.core2.color import ColorVector
from lux.core2.main import CoordSpace, Instruction
from lux.core2.timely import TimeInstant


class ChaserInstruction(Instruction[int]):
  def getColorAtPoint(self, point: int, instant: TimeInstant, coordSpace: CoordSpace[int]) -> ColorVector:
    bound = coordSpace.bounds[1]
    value = floor(((instant.time*100 % bound) + point) % bound / bound * 255)
    return [value, value, value]
 