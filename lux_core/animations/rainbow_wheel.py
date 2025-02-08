from colorsys import hsv_to_rgb
from lux_core.color import ColorVector
from dataclasses import dataclass
import functools
from math import floor
from typing import Any, Callable, Concatenate, Coroutine, Protocol, Tuple
from lux_core.context import LuxContext
from lux_core.iris.instruction_registry import TimeColorFunction, TickData
from asyncio import sleep
import time

from lux_core.diag.frame_counting import FrameCounterThread
from lux_core.color import Color
from lux_core.nonopt.framerate_rectifier import FramerateRectifier
from lux_core.iris.instruction_registry import TimeColorFunction, RegistryFunction

async def run_framed_instruction(
  fn: TimeColorFunction,
  context: LuxContext,
  *args: ...
):
  try:
    counter_thread = None
    if context.debug_display:
      counter_thread = FrameCounterThread(do_total=True)
      counter_thread.start()

    frame_clock = FramerateRectifier()
    frame_clock.target_fps = context.target_fps

    while True:
      display = context.display

      t = time.time()
      for i in range(display.length):
        display.setPixel(
          i,
          Color(fn(TickData(t, i/display.length), *args))
        )
      display.render()

      if context.debug_display and counter_thread:
        counter_thread.inc_count()

      await sleep(0)
      frame_clock.tick()
      await sleep(0)
  finally:
    if counter_thread is not None:
      counter_thread.stop()

def rainbow_wheel(data: TickData, interval = 1.0):
  offset = data.time % interval / interval
  t = (data.pos + offset) % 1
  return Color(ColorVector((floor(x * 255) for x in hsv_to_rgb(t, 1.0, 1.0))))

rainbow_wheel_instr = functools.partial(run_framed_instruction, rainbow_wheel)

async def run_instant_instruction(fn: TimeColorFunction, context: LuxContext, *args: ...):
  display = context.display
  t = time.time()
  for i in range(display.length):
    display.setPixel(i, fn(TickData(t, i/display.length), *args))
  display.render()

clear = functools.partial(run_instant_instruction, lambda _: Color(0,0,0))

def _fill(_: TickData, fill_color: Color):
  return fill_color

fill = functools.partial(run_instant_instruction, _fill)