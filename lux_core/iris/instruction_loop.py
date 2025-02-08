from asyncio import CancelledError, Task, create_task, ensure_future, run, sleep
import asyncio
from dataclasses import dataclass
import inspect
import time
import traceback
from typing import Callable, Union
from lux_core.animations.rainbow_wheel import rainbow_wheel_instr, clear, fill
from lux_core.beam.core import Instruction, RawInstruction
from lux_core.context import LuxContext
from lux_core.diag.frame_counting import FrameCounterThread
from lux_core.gui_display import PixelGuiDisplay
from lux_core.iris.event import DataEvent
from lux_core.iris.instruction_parser import parse_params
from lux_core.logging import get_logger

from lux_core.color import Color
from lux_core.display import Display
from lux_core.nonopt.framerate_rectifier import FramerateRectifier
from lux_core.iris.instruction_registry import InstructionRegistry, RegistryInstructionMetadata, TimeColorFunction


  
# FIXME
app_context: LuxContext

# TODO should this be either or? Raw or non?
class ReceivedInstructionEvent(DataEvent[Instruction]):
  pass

# FIXME
interval = 5.0

reg = InstructionRegistry()

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

    task: Union[Task, None] = None

    while True:
      data = await event.waitForValue()
      logger.debug(f"Event received: {data!r}")

      # Event was consumed, clear and continue
      event.clear()

      i_reg = reg.get(data.id)

      if i_reg is None:
        logger.warning(f"Could not find instruction with id '{data.id!r}'. Ignoring received event..")
        continue
      
      i_fn = i_reg.func
      params = parse_params(data.parameters, i_reg.param_parsers)

      if task is not None and not task.done():
        logger.debug("Cancelling previous task")
        task.cancel()
    

      task = ensure_future(i_fn(app_context, *params))
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

  reg["rwheel"] = RegistryInstructionMetadata(
    rainbow_wheel_instr,
    [float]
  )
  reg["clear"] = RegistryInstructionMetadata(clear)
  reg["fill"] = RegistryInstructionMetadata(
    fill,
    [Color.fromHexString]
  )

  async def main():

    (loop, event) = create_instruction_loop()

    ensure_future(loop())

    await sleep(0.5)

    event.setWithValue(Instruction("fill", ['012345']))

    await sleep(0.5)

    event.setWithValue(Instruction("fill", ['ff00ff']))
    
    event.setWithValue(Instruction("rwheel"))

    await sleep(3)

    event.setWithValue(Instruction("clear"))

    await sleep(2)

    event.setWithValue(Instruction("rwheel", ['5.0', '123']))

    while True:
      await sleep(0.1)

  run(main())
  