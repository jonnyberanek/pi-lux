import random

from lux.app.instructions.helpers import lerpColor
from lux.core2.main import ColorVector, CoordSpace, Instruction, TimeInstant
from lux.app.util.time_util import Intervaled


def getBrightColor():
  # Guarantees a bright color,
  # Shuffles which color is set to max and then distributes values among
  # the other two
  color = [0,0,0]
  colorIndexPrio = [x for x in range(0,3)]
  random.shuffle(colorIndexPrio)
  color[colorIndexPrio[0]] = 255
  color[colorIndexPrio[1]] = random.randrange(0,256)
  # So we can get colors like 255,0,0, but never have a sum total higher than 512
  color[colorIndexPrio[2]] = min(random.randrange(0,256), 255 - color[colorIndexPrio[1]])
  return color

BOTTOM = [10,10,10]

class DaintyFadeInOutInstruction(Instruction[int], Intervaled):

  interval: float = 3
  targetColor: list[int]

  def __init__(self) -> None:
    super().__init__()
    self.targetColor = getBrightColor()
    self.currentInterval = 0

  def getColorAtPoint(self, point: int, instant: TimeInstant, coordSpace: CoordSpace[int]) -> ColorVector:
    iinstant = self.getIntervalTimeInstant(instant)
    # Get a new color if we are on a new interval
    if (iinstant.time // self.interval) != self.currentInterval:
      self.currentInterval = iinstant.time // self.interval
      self.targetColor = getBrightColor()

    # Split the interval into two halves
    colorspacePct = iinstant.intervalPercent * 2 % 1
    if (iinstant.intervalTime >= self.interval/2.0):
      colorspacePct = 1 - colorspacePct
    
    return lerpColor(BOTTOM, self.targetColor, colorspacePct)