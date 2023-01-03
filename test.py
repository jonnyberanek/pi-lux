from lux.app.animations.dainty_rainbow import randomRainbowFadeInOut
# from lux.app.animations.rainbow_chaser import rainbowChaser
from test_animations.dainty_rainbow import DaintyFadeInOutAnimation
from test_animations.rainbow_chaser import RainbowChaserAnimation
from lux.app.app_writer import getAppPixelWriter
# from lux.core.animation import Animator
import asyncio
import threading
from queue import Queue
import time
from typing import Coroutine

from test_animations.shared import Animation, Animator

print_lock = threading.Lock()

class AnimationHelper():

  STOP_ANIMATION = "STOP"

  animation: Animator
  nextAnimation: Animation = None

  def __init__(self, animator: Animator, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.animator = animator

  def run(self):
    print (threading.current_thread().name)
    while True:
      if self.nextAnimation == AnimationHelper.STOP_ANIMATION:
        self.nextAnimation = None
        self.animator.clearAnimation()
        continue
      if self.nextAnimation != None:
        print(f"Running {self.nextAnimation}")
        self.animator.setAnimation(self.nextAnimation)
        self.nextAnimation = None
      if self.animator.currentAnimation != None :
        self.animator.renderFrame()
        time.sleep(self.animator.frameTime)
      else:
        print("No command")
        time.sleep(0.2)

  def animate(self, message):
    if self.receive_messages:
      with print_lock:
        print (threading.currentThread().getName(), "Received {}".format(message))

class CommandThread(threading.Thread):

  animThread: AnimationHelper

  def __init__(self, animThread, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.animThread = animThread

  def run(self) -> None:
    time.sleep(0.5)
    self.sendCommand(RainbowChaserAnimation(20, 3, 10))
    time.sleep(2)
    self.sendCommand(AnimationHelper.STOP_ANIMATION)
    time.sleep(2)
    self.sendCommand(DaintyFadeInOutAnimation(20,3))

  def sendCommand(self, cmd: str):
    print("Sending command: {}".format(cmd))
    self.animThread.nextAnimation = cmd

"""
class FakeRunner():

  async def runCommand(self, cmd: str):
    while True:
      print("Running {}".format(cmd))
      await asyncio.sleep(0.2)
    

class AsyncioCommandThread(threading.Thread):
  # Mocks an asyncronous input like an http server

  # loop: asyncio.ProactorEventLoop
  runner: FakeRunner
  coro: Coroutine = None

  def __init__(self, loop, runner, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    
    self.runner = runner

  def run(self) -> None:
    self.loop = asyncio.new_event_loop()
    asyncio.set_event_loop(self.loop)
    time.sleep(0.5)
    self.sendCommand("Jump")
    time.sleep(2)
    self.sendCommand("Wave")

  def sendCommand(self, cmd: str):
    # if(self.current != None):
    #   try:
    #     self.current.close()
    #   except Exception as e:
    #     print(e) 
    print("Sending command: {}".format(cmd))
    # self.coro = 
    self.loop.create_task(self.runner.runCommand(cmd))
    # asyncio.ensure_future(self.coro)

class App():

  loop: asyncio.BaseEventLoop

  def __init__(self) -> None:
    self.loop = asyncio.new_event_loop()

  def start(self):
    AsyncioCommandThread(self.loop, FakeRunner()).start()
    time.sleep(5)
"""


if __name__ == '__main__':
  leds = getAppPixelWriter()
  animator = Animator(leds, frequency=30)

  # # Threading
  thread = AnimationHelper(animator)

  cmdThread = CommandThread(thread)
  cmdThread.start()
  thread.run()

  # time.sleep(5)


  # Asyncio
  # idfk


  # animator.startAnimation(DaintyFadeInOutAnimation(leds.display.numPixels,3))

  # start = time.time()

  # while (time.time() - start) < 3:
  #  deltaTime = time.time() - start
  # #  print(f"{deltaTime:.2f}", simpleTick(deltaTime))
  # #  print(f"{deltaTime:.2f}", animation.getFrame(deltaTime))



  #  time.sleep(0.2)
  #  print("")

  # animator.startAnimation(randomRainbowFadeInOut())
