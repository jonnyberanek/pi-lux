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

# Define rainbow cycle function to do a cycle of all hues.
def rainbowChaser():
  def gen(writer: PixelDisplayWriter):
    while True:
      for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(writer.display.numPixels):
          writer.display.setPixel(i, wheel(((i * 256 // writer.display.numPixels) + j) % 256))
        writer.display.show()
        yield
  return gen


def intToColor(value: int):
  match value:
    case 0:
      return "r"
    case 1:
      return "g"
    case 2:
      return "b"     


interval = 2
size = 7
outRange = 256
loopSize = 7

def simpleTick(time: float):
  intervalPos = time % interval
  intervalPct = intervalPos / interval

  firstValue = int(intervalPct*outRange)

  print(intervalPos, intervalPct, firstValue)

  oList = []
  for i in range(0,size):

    pctOfLoop = ((intervalPos + i) % loopSize) / loopSize

    pos = int(pctOfLoop * outRange % outRange)

    oList.append(pos)
  return oList



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
