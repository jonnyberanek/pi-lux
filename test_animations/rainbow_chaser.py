from lux.core.strip import PixelDisplayWriter
from test_animations.shared import Animation

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
class RainbowChaserAnimation(Animation):

  loopSize: int

  def __init__(self, size: int, interval: float, loopSize: int) -> None:
    super().__init__(size, interval)
    self.loopSize = loopSize
  

  def _animate(self, intervalTime, time):
    oList = []

    intervalStart = intervalTime/self.interval
    for i in range(0, self.size):
      
      colorspacePct = intervalStart + ((i% self.loopSize)/self.loopSize) 
      pos = int(colorspacePct * COLOR_MAX % COLOR_MAX)

      oList.append(wheel(pos))
    return oList
