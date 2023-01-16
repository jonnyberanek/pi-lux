import random
from lux.app.animations.helpers import lerpColor

from lux.core.strip import PixelDisplayWriter
from test_animations.shared import Animation


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
class DaintyFadeInOutAnimation(Animation):

  targetColor: list[int]
  currentInterval: int

  def __init__(self, size: int, interval: float) -> None:
    super().__init__(size, interval)
    self.targetColor = getBrightColor()
    self.currentInterval = 0

  def _animate(self, intervalTime: float, time: float):
    # Get a new color if we are on a new interval
    if (time // self.interval) != self.currentInterval:
      self.currentInterval = time // self.interval
      self.targetColor = getBrightColor()

    # Split the interval into two halves
    colorspacePct = (intervalTime / self.interval * 2) % 1
    if (intervalTime >= self.interval/2.0):
      colorspacePct = 1 - colorspacePct
    
    return lerpColor(BOTTOM, self.targetColor, colorspacePct)
