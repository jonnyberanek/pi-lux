from colorsys import hsv_to_rgb
import functools
from math import floor
from typing import Callable
from lux_core.context import LuxContext
from lux_core.iris.instruction_registry import TimeColorFunction
from asyncio import sleep
import time

from lux_core.diag.frame_counting import FrameCounterThread
from lux_core.color import Color
from lux_core.nonopt.framerate_rectifier import FramerateRectifier
from lux_core.iris.instruction_registry import TimeColorFunction

async def run_framed_instruction(
  fn: TimeColorFunction,
  context: LuxContext,
  *args: ...
):

  interval = 5.0
  try:
    counter_thread = None
    if context.debug_display:
      counter_thread = FrameCounterThread(do_total=True)
      counter_thread.start()

    frame_clock = FramerateRectifier()
    frame_clock.target_fps = context.target_fps

    while True:
      pos = time.time() % interval
      display = context.display

      for i in range(display.length):
        t = ((i / display.length) * interval + pos) % interval / interval
        display.setPixel(i, Color(fn(t, *args)))
      display.render()

      if context.debug_display:
        counter_thread.inc_count()

      await sleep(0)
      frame_clock.tick()
      await sleep(0)
  finally:
    if counter_thread is not None:
      counter_thread.stop()

rainbow_wheel: TimeColorFunction = lambda t: tuple((floor(x * 255) for x in hsv_to_rgb(t, 1.0, 1.0)))

rainbow_wheel_instr = functools.partial(run_framed_instruction, rainbow_wheel)

async def run_instant_instruction(fn: TimeColorFunction, context: LuxContext, *args: ...):
  display = context.display
  for i in range(display.length):
    display.setPixel(i, fn(time.time(), *args))
  display.render()

clear = functools.partial(run_instant_instruction, lambda _: Color(0,0,0))