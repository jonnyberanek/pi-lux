import asyncio
from typing import Generic, TypeVar, Union
from lux_core.animations import boot_sequence
from lux_core.beam.core import Instruction
from lux_core.beam.server import create_beam_server
from lux_core.logging import get_logger, init_logging

from lux_core.color import Color, rgb_to_rbg
from lux_core.display import Display
from lux_core.nonopt.framerate_rectifier import FramerateRectifier

if __name__ == "__main__":
  init_logging()

logger = get_logger(__name__)

loop = asyncio.get_event_loop()

T = TypeVar("T")

class LuxContext:
  display: Display
  
app_context = LuxContext()
try:
  import board
  from adafruit_ws2801 import WS2801

  class LinearWS2801Display(WS2801, Display):
    def __init__(self, *args, **kwargs) -> None:
      super().__init__(*args, **kwargs)

    def render(self):
      return self.show()
    
    def setPixel(self, index: int, color: Color):
      self[index] = rgb_to_rbg(color)

    @property
    def length(self) -> int:
      return len(self)

  odata = board.MOSI
  oclock = board.SCLK
  numleds = 46
  bright = 1.0
  app_context.display = LinearWS2801Display(
      oclock, odata, numleds, brightness=bright, auto_write=False
  )
except Exception as e:
  from lux_core.gui_display import PixelGuiDisplay
  logger.info("Failed to initialize physical display: %s", e)
  app_context.display = PixelGuiDisplay(20)

class ADataEvent(asyncio.Event, Generic[T]):
  """
  This retains a value with an asynchronous event until it is cleared. This has
  the opportunity to drop events if "overwritten" by a subsequent `set` before
  it can be consumed. This is expected, this should be used in a realtime
  system, prefer `asyncio.Queue` otherwise.
  """
  data: Union[T | None] = None

  def setWithValue(self, value: T):
    self.data = value
    return self.set()

  def clear(self):
    self.data = None
    return super().clear()
  
  async def waitForValue(self) -> T:
    await super().wait()
    return self.data
  
class ReceivedInstructionEvent(ADataEvent[Instruction]):
  pass

aevent = ReceivedInstructionEvent()

async def listen_for_instructions():
  logger = get_logger("instr_reader")
  logger.info("Ready to receive events...")
  while True:
    data = await aevent.waitForValue()
    c = Color.fromHexString(data.parameters[0])
    logger.debug(f"Event received with: {c.toHex()}")
    aevent.clear()

    display = app_context.display

    for i in range(display.length):
      display.setPixel(i, c)
    display.render()

interval = 5
target_fps = 30



def handle_instructions(instr: list[Instruction]):
  aevent.setWithValue(instr[-1:][0])

async def do_things():
  asyncio.ensure_future(listen_for_instructions())
  server = await create_beam_server(handle_instructions)

  boot_sequence.run(app_context.display, interval)

  async with server:
    await server.serve_forever()

if __name__ == "__main__":
  loop.run_until_complete(do_things())