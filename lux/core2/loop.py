from abc import ABC, abstractmethod
from time import sleep, time


class GameLoop(ABC):

  def processInput(self):
    pass
  
  def update(self):
    pass

  def render(self):
    pass

class LoopRunner(ABC):

  @abstractmethod
  def run(self, loop: GameLoop):
    pass

class FixedStepRunner(LoopRunner):

  def __init__(self, msPerUpdate: int) -> None:
    super().__init__()
    self.secPerUpdate = msPerUpdate / 1000

  def run(self, loop: GameLoop):
    previous = time()
    lag = 0
    while True:
      current = time()
      elapsed = current - previous
      previous = current
      lag += elapsed

      loop.processInput()

      while lag >= self.secPerUpdate:
        loop.update()
        lag -= self.secPerUpdate
      
      loop.render()

class ThrottledFixedStepRunner(LoopRunner):

  def __init__(self, msPerUpdate: int, maxFps: int = 120) -> None:
    super().__init__()
    self.secPerUpdate = msPerUpdate / 1000
    self.minFrameTime = 1/maxFps

  def run(self, loop: GameLoop):
    previous = time()
    lastRender = time()
    lag = 0
    while True:
      current = time()
      elapsed = current - previous
      previous = current
      lag += elapsed

      loop.processInput()

      while lag >= self.secPerUpdate:
        loop.update()
        lag -= self.secPerUpdate
      
      loop.render()
      currentRender = time()

      if(currentRender - lastRender < self.minFrameTime):
        sleep(self.minFrameTime - (currentRender - lastRender))
      lastRender = currentRender