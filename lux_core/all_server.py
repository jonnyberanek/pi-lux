import asyncio
from typing import Generic, TypeVar, Union
from lux_core.animations import boot_sequence
from lux_core.beam.core import Instruction
from lux_core.beam.server import create_beam_server
from lux_core.iris.instruction_loop import create_instruction_loop
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

interval = 5
target_fps = 30

async def do_things():
  (run_loop, event) = create_instruction_loop()

  asyncio.ensure_future(run_loop())

  server = await create_beam_server(
    lambda instr: event.setWithValue(instr[-1:][0])
  )

  boot_sequence.run(app_context.display, interval)

  async with server:
    await server.serve_forever()

if __name__ == "__main__":
  loop.run_until_complete(do_things())