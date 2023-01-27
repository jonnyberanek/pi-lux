import time

from lux.app.util.frame_benchmark import FrameBenchmark
from lux.core2.instruction_provider import InstructionProvider
from lux.core2.loop import GameLoop
from lux.core2.main import Coordinator
from lux.core2.timely import TimeInstant

class CoordinatorGameLoop(GameLoop):

  animationStart = 0

  def __init__(self, coordinator: Coordinator, inputProvider: InstructionProvider) -> None:
    self.coordinator = coordinator
    self.inputProvider = inputProvider
    self.benchmark = FrameBenchmark(100)

  def processInput(self):
    instruction = self.inputProvider.consumeInstruction()
    if instruction == None:
      return
    if instruction == InstructionProvider.STOP:
      self.coordinator.instruction = None
      self.coordinator.clear()
      self.coordinator.render()
      return
    self.animationStart = time.time()
    self.coordinator.instruction = instruction

  def update(self):
    if self.coordinator.instruction == None:
      return
    self.coordinator.runInstruction(
      TimeInstant(time.time() - self.animationStart)
    )
    
  def render(self):
    if self.coordinator.instruction == None:
      return
    self.coordinator.render()
    self.benchmark.add()
    self.benchmark.logTime()