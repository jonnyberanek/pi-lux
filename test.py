from abc import ABC, abstractmethod
from queue import Queue
import threading
import time
from typing import Union
from gameloop_test import GameLoop, ThrottledFixedStepRunner
from lux.app.app_writer import getAppPixelDisplay

from lux.app.coordinator import DynamicNotCoordinator, NotCoordinator, SimpleCoordinator
from lux.app.instructions.dainty_rainbow import DaintyFadeInOutInstruction
from lux.app.instructions.rainbow_chaser import RainbowChaserInstruction
from lux.app.util.frame_benchmark import FrameBenchmark
from lux.core2.main import Instruction
from lux.core2.timely import TimeInstant

FREQ = 30
FRAME_TIME = 1/FREQ

def getLast(queue: Queue):
  last = None
  while not queue.empty():
    last = queue.get()
  return last

class InstructionProvider(ABC):
  STOP = "STOP"

  @abstractmethod
  def consumeInstruction(self) -> Union[Instruction, str, None]:
    pass
  
  @abstractmethod
  def setInstruction(self, instruction: Instruction):
    pass

class QueueInstructionProvider(InstructionProvider):

  def __init__(self, queue: Queue) -> None:
    super().__init__()
    self.queue = queue

  def consumeInstruction(self):
    lastInstruction = getLast(self.queue)
    if lastInstruction == None:
      return None
    return lastInstruction
  
  def setInstruction(self, instruction: Instruction):
    self.queue.put(instruction)

class DisplayGameLoop(GameLoop):

  animationStart = 0

  def __init__(self, inputProvider: InstructionProvider) -> None:
    self.coordinator = DynamicNotCoordinator(getAppPixelDisplay())
    self.inputProvider = inputProvider
    self.benchmark = FrameBenchmark(100)

  def processInput(self):
    instruction = self.inputProvider.consumeInstruction()
    if instruction == None:
      return
    if instruction == InstructionProvider.STOP:
      self.coordinator.instruction = None
      self.coordinator.clearDisplays()
      self.render()
      return
    self.animationStart = time.time()
    self.coordinator.instruction = instruction

  def update(self):
    if self.coordinator.instruction == None:
      return
    self.coordinator.setPixels(
      self.coordinator.calcPixels(TimeInstant(time.time() - self.animationStart))
    )
    
  def render(self):
    if self.coordinator.instruction == None:
      return
    self.coordinator.updateDisplay()
    self.coordinator.render()
    self.benchmark.add()
    self.benchmark.logTime()

class CommandThread(threading.Thread):

  def __init__(self, inputProvider, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.inputProvider = inputProvider 
  
  def run(self) -> None:
    time.sleep(0.5)
    self.inputProvider.setInstruction(RainbowChaserInstruction(10))
    time.sleep(2)
    self.inputProvider.setInstruction(InstructionProvider.STOP)
    time.sleep(2)
    self.inputProvider.setInstruction(DaintyFadeInOutInstruction())

if __name__ == '__main__':

  qip = QueueInstructionProvider(Queue())
  commandThread = CommandThread(qip)
  gameloop = DisplayGameLoop(qip)

  commandThread.start()
  ThrottledFixedStepRunner(32, 60).run(gameloop)

  # display = getAppPixelDisplay()
  # coordinator = NotCoordinator(display, DaintyFadeInOutInstruction())
  # print(f"Animator frames is {FREQ}")

  # AnimationManager(coordinator).run()
