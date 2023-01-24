
from abc import ABC, abstractmethod
from math import floor
from time import sleep, time
import os
from typing import Callable, List, TypeVar

from lux.app.app_writer import getAppPixelDisplay
from lux.app.coordinator import NotCoordinator
from lux.app.instructions.dainty_rainbow import DaintyFadeInOutInstruction
from lux.app.util.frame_benchmark import FrameBenchmark
from lux.core2.timely import TimeInstant
clear = lambda: os.system("cls")

LOADER = "\\|/-"

class GameLoop(ABC):

  def process(self):
    pass
  
  def update(self):
    pass

  def render(self):
    pass

class LoopRunner(ABC):

  @abstractmethod
  def run(self, loop: GameLoop):
    pass

class SerialRunner(LoopRunner):

  def __init__(self, msPerFrame: int) -> None:
    super().__init__()
    self.secPerFrame = msPerFrame / 1000

  def run(self, loop: GameLoop):
    while True: 
      start = time()
      loop.process()
      loop.update()
      loop.render()
      diff = start + self.secPerFrame - time()
      print(diff)
      sleep(max(diff, 0))

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

      loop.process()

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

      loop.process()

      while lag >= self.secPerUpdate:
        loop.update()
        lag -= self.secPerUpdate
      
      loop.render()
      currentRender = time()

      if(currentRender - lastRender < self.minFrameTime):
        sleep(self.minFrameTime - (currentRender - lastRender))
      lastRender = currentRender


class TestGameLoop(GameLoop):

  letterOs = "o"

  def update(self):
    # clear()
    # print(LOADER[floor(time() * 10 % 4)])
    if(len(self.letterOs) > 15):
      self.letterOs = ""
    self.letterOs += "o" 

  def render(self):
    # clear()
    # print(f"Hell{self.letterOs}!")
    sleep(len(self.letterOs)/100)

class DisplayGameLoop(GameLoop):

  def __init__(self) -> None:
    display = getAppPixelDisplay()
    self.coordinator = NotCoordinator(display, DaintyFadeInOutInstruction())
    self.start = time()
    self.benchmark = FrameBenchmark(100)
  
  def update(self):
    self.coordinator.setPixels(
      self.coordinator.calcPixels(TimeInstant(time() - self.start))
    )
    
  def render(self):
    self.coordinator.updateDisplay()
    self.coordinator.render()
    self.benchmark.add()
    self.benchmark.logTime()


ThrottledFixedStepRunner(32, 60).run(DisplayGameLoop())