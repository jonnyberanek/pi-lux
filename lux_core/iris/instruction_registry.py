import asyncio
from time import ctime
from typing import Callable

from lux_core.color import ColorVector

TimeColorFunction = Callable[[float, int], ColorVector]
#TODO figure out how to replace ... with [LuxContext, ...]
RegistryFunction = Callable[..., TimeColorFunction]

class InstructionRegistry(dict[str, RegistryFunction]):
  """
  Used to store how instructions map to functionality.
  Given a key (instruction identifier), map to a something that is used by other parts of the app
  """
  pass

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
  