import asyncio
import collections
import collections.abc
from dataclasses import dataclass, field
import inspect
from time import ctime
from typing import Any, Callable, Concatenate, Coroutine, Tuple
from lux_core.color import Color, ColorVector
from lux_core.context import LuxContext
from lux_core.iris.instruction_parser import ParseFunc

# I don't think is designed well, but idc. I need a quick & easy way to parse args
    

@dataclass
class TickData():
  time: float
  """Where the pixel is located in a space from 0 to 1, typical the index normalized on total length"""
  pos: float

TimeColorFunction = Callable[Concatenate[TickData, ...], Color]
#TODO figure out how to replace ... with [LuxContext, ...]
x = collections.abc
RegistryFunction = Callable[Concatenate[LuxContext, ...], Coroutine[Any, Any, None]]

@dataclass
class RegistryInstructionMetadata:
  func: RegistryFunction
  # TODO review, not sure that this feels correct, should parsers be set at start?
  param_parsers: list[ParseFunc] = field(default_factory=lambda: [])

class InstructionRegistry(dict[str, RegistryInstructionMetadata]):
  """
  Used to store how instructions map to functionality.
  Given a key (instruction identifier), map to a something that is used by other parts of the app
  """

if __name__ == "__main__":
  # reg = InstructionRegistry()
  # reg["fill"] = 20
  # reg["asdasd"] = 2134

  # ## later in app
  # # reg = get_reg()
  # instr = Instruction()
  # ii = reg.get(instr.id)
  # if ii is None:
  #   raise Exception("TODO does not exist")
  
  # two possibilities: app uses it instruction in instant (async still), or
  # starts up thread (or future) to run long-running task
  
  async def loop():
    waits = 0
    print(f"{waits} - {ctime()}")
    
    while True:
      await asyncio.sleep(0.5)
      waits += 1
      print(f"{waits} - {ctime()}")

  async def main():
    task = asyncio.create_task(loop())
    await asyncio.sleep(1.6)
    print(f"Cancel result: {task.cancel()}")

  asyncio.run(main())
  