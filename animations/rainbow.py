import random
from pixlr.strip import PixelStripWriter

"""
Lerp Helpers
"""
def lerp(i, f, t):
  return i + (f-i) * t

def lerpi(i,f,t):
  return int(lerp(i,f,t))

def lerpColor(i, f, t):
  return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))

def getBrightColor():
  # Guarantees a bright color,
  # Shuffles which color is set to max and then distributes values among
  # the other two
  color = [0,0,0]
  colorIndexPrio = [x for x in range(0,3)]
  random.shuffle(colorIndexPrio)
  color[colorIndexPrio[0]] = 255
  color[colorIndexPrio[1]] = random.randrange(0,256)
  color[colorIndexPrio[2]] = 255 - color[colorIndexPrio[1]]
  return color

def randomRainbowFade(transitionFrames=15):
  def gen(writer: PixelStripWriter):
    while True:
      target = getBrightColor()
      print(target)
      for i in range(0,transitionFrames):
        writer.fill(lerpColor([0,0,0], target, i/transitionFrames))
        yield
      writer.fill(target)
      yield
      for i in range(0,transitionFrames):
        writer.fill(lerpColor(target, [0,0,0], i/transitionFrames))
        yield
      writer.fill([0,0,0])
      yield
  return gen