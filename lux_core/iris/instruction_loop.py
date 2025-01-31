from asyncio import CancelledError, Task, create_task, ensure_future, run, sleep
import asyncio
from dataclasses import dataclass
import time
import traceback
from typing import Callable, Union
from lux_core.animations.rainbow_wheel import rainbow_wheel_instr, clear
from lux_core.beam.core import Instruction
from lux_core.context import LuxContext
from lux_core.diag.frame_counting import FrameCounterThread
from lux_core.gui_display import PixelGuiDisplay
from lux_core.iris.event import DataEvent
from lux_core.logging import get_logger

from lux_core.color import Color
from lux_core.display import Display
from lux_core.nonopt.framerate_rectifier import FramerateRectifier
from lux_core.iris.instruction_registry import InstructionRegistry, TimeColorFunction


  
# FIXME
app_context: LuxContext

class ReceivedInstructionEvent(DataEvent[Instruction]):
  pass

# FIXME
interval = 5.0

reg = InstructionRegistry()

async def run_longterm_instruction(fn: TimeColorFunction):

  if not callable(fn):
    display = app_context.display
    for i in range(display.length):
      display.setPixel(i, Color(fn))
    display.render()
    return

  try:
    counter_thread = None
    if app_context.debug_display:
      counter_thread = FrameCounterThread(do_total=True)
      counter_thread.start()

    frame_clock = FramerateRectifier()
    frame_clock.target_fps = app_context.target_fps

    while True:
      pos = time.time() % interval
      display = app_context.display

      for i in range(display.length):
        t = ((i / display.length) * interval + pos) % interval / interval
        display.setPixel(i, Color(fn(t)))
      display.render()

      if app_context.debug_display:
        counter_thread.inc_count()

      await sleep(0)
      frame_clock.tick()
      await sleep(0)
  finally:
    counter_thread.stop()

def create_instruction_loop():
  event = ReceivedInstructionEvent()
  
  logger = get_logger("instr_reader")

  def listen_to_task(task: Task):
    if task.cancelled():
      logger.debug(f"{task.get_name()}: Cancelled")
    elif task.exception() is not None:
      logger.debug(
        f"{task.get_name()}: Ended in exception",
        exc_info=task.exception()
      )
    else:
      logger.debug(f"{task.get_name()}: Task was success??")

  async def run_loop(): 
    logger.info("Ready to receive events...")

    task: Union[Task | None] = None

    while True:
      data = await event.waitForValue()
      logger.debug(f"Event received: {data!r}")

      # Event was consumed, clear and continue
      event.clear()

      i_fn = reg.get(data.id)

      if i_fn is None:
        logger.warning(f"Could not find instruction with id '{data.id!r}'. Ignoring received event..")
        continue

      logger.debug(i_fn)

      if task is not None and not task.done():
        logger.debug("Cancelling previous task")
        task.cancel()
        # else:
        #   if task.cancelled():
        #     logger.debug("previous task cancelled")
        #   elif task.exception is not None:
        #     logger.debug(f"previous task ended in exception", exc_info=task.exception)
        #   else:
        #     logger.debug(f"previous task was success??")

      # TODO pass in parameters
      task = ensure_future(i_fn(app_context))
      task.set_name(f"{data.id}_task-{time.time_ns()}")
      task.add_done_callback(listen_to_task)

  return (run_loop, event)

if __name__ == "__main__":
  from lux_core.logging import init_logging
  init_logging()

  app_context = LuxContext(
    display=PixelGuiDisplay(20),
    debug_display=True
  )

  reg["rwheel"] = rainbow_wheel_instr
  reg["clear"] = clear

  async def main():

    (loop, event) = create_instruction_loop()

    ensure_future(loop())

    await sleep(0.5)
    
    event.setWithValue(Instruction("rwheel"))

    await sleep(3)

    event.setWithValue(Instruction("clear"))

    await sleep(2)

    event.setWithValue(Instruction("rwheel"))

    while True:
      await sleep(0.1)

  run(main())
  