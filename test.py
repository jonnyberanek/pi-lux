from queue import Queue
import threading
import time
from lux.app.app_writer import getAppPixelDisplay

from lux.app.coordinator import NotCoordinator, SimpleCoordinator
from lux.app.instructions.dainty_rainbow import DaintyFadeInOutInstruction
from lux.app.instructions.rainbow_chaser import RainbowChaserInstruction
from lux.app.util.frame_benchmark import FrameBenchmark
from lux.core2.main import Instruction
from lux.core2.timely import TimeInstant

FREQ = 30
FRAME_TIME = 1/FREQ

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

  @property
  def currentInstruction(self):
    return self.coordinator.instruction

  @currentInstruction.setter
  def currentInstruction(self, animation: Instruction):
    self.animationStartTime = time.time()
    self.coordinator.instruction = animation

  def clearAnimation(self):
    self.animationStartTime = None
    self.coordinator.instruction = None
    self.coordinator.clearDisplays()

  def requestFrame(self):
    deltaTime = time.time() - self.animationStartTime
    self.coordinator.updateDisplays(TimeInstant(deltaTime))

  def render(self):
    self.coordinator.render() # TODO incorrect

class AnimationManager():

  STOP_ANIMATION = "STOP"

  # # TODO: make setter instead of direct assignment (Can maybe obscure that a null means "stop" or something)
  # nextInstruction: Instruction = None

  # def setNextInstruction(self, next: Instruction):
  #   self.nextInstruction = next

  def __init__(self, coordinator: NotCoordinator, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.coordinator = coordinator

  def run(self):
    print (f"[{threading.current_thread().name}] AnimationManager is running")
    benchmark = FrameBenchmark(FREQ)
    queue = Queue()
    computeThread = ComputeThread(self.coordinator, queue)
    computeThread.start()
    while True:
      # if self.nextInstruction == AnimationManager.STOP_ANIMATION:
      #   self.nextInstruction = None
      #   # self.animator.clearAnimation()
      #   continue
      # if self.nextInstruction != None:
      #   print(f"Running {self.nextInstruction}")
      #   self.coordinator.instruction = self.nextInstruction
      #   self.nextInstruction = None
      # if self.coordinator.instruction != None :
        # computeThread.requestFrame()
      benchmark.add()
      benchmark.logTime()
      computeThread.requestFrame()
      time.sleep(FRAME_TIME)
      recentItem = None
      while not queue.empty():
        recentItem = queue.get()
      if recentItem != None:
        coordinator.setPixels(recentItem)
        coordinator.updateDisplay()
        coordinator.render()
      # else:
      #   print("No command")
      #   time.sleep(0.2)

class ComputeThread(threading.Thread):

  def __init__(self, coord: NotCoordinator, queue: Queue, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.coord = coord
    self.frameRequested = None
    self.queue = queue
  
  def requestFrame(self):
    if(self.frameRequested != None):
      print("Frame dropped?")
    self.frameRequested = time.time()
  
  def run(self) -> None:
    print (f"[{threading.current_thread().name}] Compute Thread runnning")
    start = time.time()
    while True:
      if(self.frameRequested != None):
        pxs = self.coord.calcPixels(TimeInstant(time.time() - start))
        self.frameRequested = None
        self.queue.put(pxs)
      time.sleep(FRAME_TIME)


class CommandThread(threading.Thread):

  animThread: AnimationManager

  def __init__(self, animThread, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.animThread = animThread

  def run(self) -> None:
    time.sleep(0.5)
    self.sendCommand(RainbowChaserInstruction(10))
    time.sleep(2)
    self.sendCommand(AnimationManager.STOP_ANIMATION)
    time.sleep(2)
    self.sendCommand(DaintyFadeInOutInstruction())

  def sendCommand(self, cmd: str):
    print("Sending command: {}".format(cmd))
    self.animThread.nextInstruction = cmd

if __name__ == '__main__':
  display = getAppPixelDisplay()
  coordinator = NotCoordinator(display, DaintyFadeInOutInstruction())
  # animator = Animator2(coordinator, frequency=30)
  # coordinator.instruction = DaintyFadeInOutInstruction()
  print(f"Animator frames is {FREQ}")

  # # Threading
  thread = AnimationManager(coordinator)

  # cmdThread = CommandThread(thread)
  # cmdThread.start()
  thread.run()
