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
      benchmark.add()
      benchmark.logTime()
      # computeThread.requestFrame()
      time.sleep(FRAME_TIME)
      recentItem = None
      while not queue.empty():
        recentItem = queue.get()
      if recentItem != None:
        coordinator.setPixels(recentItem)
        coordinator.updateDisplay()
        coordinator.render()

class ComputeThread(threading.Thread):

  def __init__(self, coord: NotCoordinator, queue: Queue, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.coord = coord
    self.frameRequested = False
    self.queue = queue
  
  def requestFrame(self):
    self.frameRequested = True
  
  def run(self) -> None:
    print (f"[{threading.current_thread().name}] Compute Thread runnning")
    start = time.time()
    while True:
      if(self.frameRequested == True):
        pxs = self.coord.calcPixels(TimeInstant(time.time() - start))
        self.frameRequested = False
        self.queue.put(pxs)
      time.sleep(FRAME_TIME)

if __name__ == '__main__':
  display = getAppPixelDisplay()
  coordinator = NotCoordinator(display, DaintyFadeInOutInstruction())
  print(f"Animator frames is {FREQ}")

  AnimationManager(coordinator).run()
