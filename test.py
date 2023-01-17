from lux.app.display_lists.gui import PixelRowGui
from lux.core.pixel import Pixel
from lux.core2.main import ColorVector, Display, IndexCoordSpace, Instruction, SimpleCoordinator
from test_animations.dainty_rainbow import DaintyFadeInOutInstruction
from test_animations.rainbow_chaser import RainbowChaserInstruction
import threading
import time

from test_animations.shared import Animation, Animator, Animator2

print_lock = threading.Lock()

class AnimationManager():

  STOP_ANIMATION = "STOP"

  animator: Animator2

  # TODO: make setter instead of direct assignment (Can maybe obscure that a null means "stop" or something)
  nextInstruction: Instruction = None

  def setNextInstruction(self, next: Animation):
    self.nextInstruction = next

  def __init__(self, animator: Animator, *args, **kwargs):
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

PIXEL_SIZE = 20

class PixelGuiDisplay(Display):

  def __init__(self, pixelsPerRow: int, rows=1) -> None:
    super().__init__()
    self.__numPixels = pixelsPerRow*rows
    self.gui = PixelRowGui(PIXEL_SIZE, pixelsPerRow, rows)
    self.coordSpace = IndexCoordSpace(self.length)

  def setPixel(self, index: int, color: ColorVector):
    self.gui.setPixel(index, Pixel(color))
  
  def render(self):
    self.gui.window.update()

  @property
  def length(self) -> int:
    return self.__numPixels

if __name__ == '__main__':
  display = PixelGuiDisplay(pixelsPerRow=20, rows=1)
  coordinator = SimpleCoordinator(display)
  animator = Animator2(coordinator, frequency=30)

  # # Threading
  thread = AnimationManager(animator)

  cmdThread = CommandThread(thread)
  cmdThread.start()
  thread.run()
