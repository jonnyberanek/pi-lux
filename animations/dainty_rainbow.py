import random
from animations.helpers import lerpColor
from ledcontroller.strip import PixelDisplayWriter

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
def randomRainbowFadeInOut(transitionFrames=15):
  
  def gen(writer: PixelDisplayWriter):
  
    while True:
      target = getBrightColor()
      for i in range(0,transitionFrames):
        writer.fill(lerpColor(BOTTOM, target, i/transitionFrames))
        yield
      writer.fill(target)
      yield
      for i in range(0,transitionFrames):
        writer.fill(lerpColor(target, BOTTOM, i/transitionFrames))
        yield
      writer.fill(BOTTOM)
      yield
  return gen
  
def randomRainbowFade(transitionFrames=15):
  
  def gen(writer: PixelDisplayWriter):
    lastTarget = getBrightColor()
    writer.fill(lastTarget)
    yield
    while True:
      target = getBrightColor()
      for i in range(0,transitionFrames):
        writer.fill(lerpColor(lastTarget, target, i/transitionFrames))
        yield
      writer.fill(target)
      lastTarget = target
  return gen