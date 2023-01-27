import threading
import time
from queue import Queue

from lux.app.app_writer import getAppPixelDisplay
from lux.app.coordinator import SingleDisplayCoordinator
from lux.app.instruction_provider import QueueInstructionProvider
from lux.app.instructions.dainty_rainbow import DaintyFadeInOutInstruction
from lux.app.instructions.rainbow_chaser import RainbowChaserInstruction
from lux.app.loops import CoordinatorGameLoop
from lux.core2.instruction_provider import InstructionProvider
from lux.core2.loop import ThrottledFixedStepRunner

class CommandThread(threading.Thread):

  def __init__(self, inputProvider, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.inputProvider = inputProvider 
  
  def run(self) -> None:
    time.sleep(0.5)
    self.inputProvider.addInstruction(RainbowChaserInstruction(10))
    time.sleep(2)
    self.inputProvider.addInstruction(InstructionProvider.STOP)
    time.sleep(2)
    self.inputProvider.addInstruction(DaintyFadeInOutInstruction())

if __name__ == '__main__':

  qip = QueueInstructionProvider(Queue())
  commandThread = CommandThread(qip)
  gameloop = CoordinatorGameLoop(SingleDisplayCoordinator(getAppPixelDisplay()), qip)

  commandThread.start()
  ThrottledFixedStepRunner(32, 60).run(gameloop)
