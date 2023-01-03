import time

from lux.core.strip import PixelDisplayWriter
from abc import abstractmethod

class Animation():

  size: int
  interval: float

  def __init__(self, size: int, interval:float) -> None:
    self.size = size
    self.interval = interval

  @abstractmethod
  def _animate(self, intervalTime: float, time: float):
    pass

  def getFrame(self, time: float):
    return self._animate(time % self.interval, time)

class Animator():
  """
  # This class composes a writer and animations to handle an animation.

  # This standardizes the animation producer and guarantees the animation never
  # depends on a specific implementation of PixelStripWriter.
  TODO
  """

  writer: PixelDisplayWriter
  currentAnimation: Animation = None
  animationStartTime: int = None

  def __init__(self, writer=None, frequency=60) -> None:
    self.writer = writer
    self.frequency = frequency

  @property
  def frameTime(self):
    return 1/self.frequency
  
  def setAnimation(self, animation: Animation):
    self.animationStartTime = time.time()
    self.currentAnimation = animation

  def clearAnimation(self):
    self.animationStartTime = None
    self.currentAnimation = None
    self.writer.fill([0,0,0])

  def renderFrame(self):
    deltaTime = time.time() - self.animationStartTime
    self.writeAnimationData(
      self.currentAnimation.getFrame(deltaTime)
    )

  def writeAnimationData(self, data):
    if(isinstance(data, list)):
      for i, x in enumerate(data):
        self.writer.display.setPixel(i, x)
        self.writer.display.show()
    else:
      self.writer.fill(data)

  def startAnimation(self, animation: Animation):
    startTime = time.time()
    while (time.time() - startTime) < 10:
      deltaTime = time.time() - startTime
      data = animation.getFrame(deltaTime)
      if(isinstance(data, list)):
        for i, x in enumerate(data):
          self.writer.display.setPixel(i, x)
          self.writer.display.show()
      else:
        self.writer.fill(data)
      time.sleep(self.frameTime)

class SimpleTickAnimation(Animation):

  loopSize = 7
  outRange = 256

  def _animate(self, intervalTime, time):
    oList = []
    for i in range(0, self.size):

      pctOfLoop = ((intervalTime + i) % self.loopSize) / self.loopSize
      pos = int(pctOfLoop * self.outRange % self.outRange)

      oList.append(pos)
    return oList