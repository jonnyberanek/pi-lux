from dataclasses import dataclass
import time
from abc import abstractmethod

from lux.core2.main import Instruction, SimpleCoordinator, TimeInstant
from lux.core.strip import PixelDisplayWriter

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

@dataclass
class IntervalTimeData(TimeInstant):
  interval: float

  @property
  def intervalTime(self):
    return self.time % self.interval

  @property
  def intervalPercent(self):
    return self.intervalTime / self.interval

class Intervaled():

  @property
  @abstractmethod
  def interval(self) -> float:
    pass
  
  def getIntervalTimeInstant(self, instant: TimeInstant):
    return IntervalTimeData(instant.time, self.interval)

class Animator():
  """
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


class Animator2():
  """
  TODO
  """
  coordinator = SimpleCoordinator #TODO determine way to keep abstract
  animationStartTime: float = None

  def __init__(self, coordinator: SimpleCoordinator, frequency=60) -> None:
    self.coordinator = coordinator
    self.frequency = frequency

  @property
  def frameTime(self):
    return 1/self.frequency
  
  def setInstruction(self, animation: Instruction):
    self.animationStartTime = time.time()
    self.coordinator.instruction = animation

  def clearAnimation(self):
    self.animationStartTime = None
    self.coordinator.instruction = None
    self.coordinator.clearDisplays()

  @property
  def currentAnimation(self):
    return self.coordinator.instruction

  def renderFrame(self):
    deltaTime = time.time() - self.animationStartTime
    self.coordinator.updateDisplays(TimeInstant(deltaTime))
