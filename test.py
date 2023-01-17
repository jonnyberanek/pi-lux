import threading
import time
from lux.app.app_writer import getAppPixelDisplay

from lux.app.coordinator import SimpleCoordinator
from lux.app.instructions.dainty_rainbow import DaintyFadeInOutInstruction
from lux.app.instructions.rainbow_chaser import RainbowChaserInstruction
from lux.core2.main import Instruction
from lux.core2.timely import TimeInstant
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

print_lock = threading.Lock()

class AnimationManager():

  STOP_ANIMATION = "STOP"

  animator: Animator2

  # TODO: make setter instead of direct assignment (Can maybe obscure that a null means "stop" or something)
  nextInstruction: Instruction = None

  def setNextInstruction(self, next: Instruction):
    self.nextInstruction = next

  def __init__(self, animator: Instruction, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.animator = animator

  def run(self):
    print (f"[{threading.current_thread().name}] AnimationManager is running")
    while True:
      if self.nextInstruction == AnimationManager.STOP_ANIMATION:
        self.nextInstruction = None
        self.animator.clearAnimation()
        continue
      if self.nextInstruction != None:
        print(f"Running {self.nextInstruction}")
        self.animator.setInstruction(self.nextInstruction)
        self.nextInstruction = None
      if self.animator.currentAnimation != None :
        self.animator.renderFrame()
        time.sleep(self.animator.frameTime)
      else:
        print("No command")
        time.sleep(0.2)

  def animate(self, message):
    if self.receive_messages:
      with print_lock:
        print(f"[{threading.current_thread().name}] Received {message}")

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
  coordinator = SimpleCoordinator(display)
  animator = Animator2(coordinator, frequency=30)

  # # Threading
  thread = AnimationManager(animator)

  cmdThread = CommandThread(thread)
  cmdThread.start()
  thread.run()
