from lux.core2.main import ColorVector, CoordSpace, Instruction, TimeInstant
from lux.app.util.time_util import Intervaled

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

COLOR_MAX = 256
class RainbowChaserInstruction(Instruction[int], Intervaled):

  interval: float = 3
  loopSize: int

  def __init__(self, loopSize: int) -> None:
    super().__init__()
    self.loopSize = loopSize

  def getColorAtPoint(self, point: int, instant: TimeInstant, coordSpace: CoordSpace[int]) -> ColorVector:
    pctInterval = self.getIntervalTimeInstant(instant).intervalPercent
    bound = coordSpace.bounds[1] # TODO: dont assume bounds[0] is 0
    pctWheel = (point + pctInterval) % bound / bound
    wheelPos = min(int(pctWheel*COLOR_MAX), COLOR_MAX)
    return wheel(wheelPos)