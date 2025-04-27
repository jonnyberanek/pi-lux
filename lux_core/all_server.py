import asyncio
from ctypes import c_ubyte
import json
from logging import DEBUG
from typing import Generic, TypeVar, Union
from lux_core.animations import boot_sequence
from lux_core.beam.core import BeamException, BeamRequest
from lux_core.beam.protocols.dfp_handler import DfpProtocolHandler
from lux_core.beam.protocols.pfp_handler import PfpProtocolHandler
from lux_core.beam.server import Result, create_beam_server
from lux_core.context import LuxContext
from lux_core.iris.instruction_loop import create_instruction_loop
from lux_core.iris.instruction_parser import ParseFunc, get_parse_type_name
from lux_core.iris.instruction_registry import InstructionRegistry, RegistryInstructionMetadata
from lux_core.logger import VERBOSE, get_logger, init_logging

from lux_core.color import Color, color_from_hex, rgb_to_rbg
from lux_core.display import Display
from lux_core.animations.rainbow_wheel import rainbow_wheel_instr, clear, fill

if __name__ == "__main__":
  init_logging(VERBOSE)

logger = get_logger(__name__)

loop = asyncio.get_event_loop()

T = TypeVar("T")
  
app_context: LuxContext
try:
  import board # pyright: ignore[reportMissingImports]
  from adafruit_ws2801 import WS2801 # pyright: ignore[reportMissingImports]

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
  app_context = LuxContext(
    display = LinearWS2801Display(
        oclock, odata, numleds, brightness=bright, auto_write=False
    )
  )
except Exception as e:
  from lux_core.gui_display import PixelGuiDisplay
  logger.info("Failed to initialize physical display: %s", e)
  app_context = LuxContext(
    display = PixelGuiDisplay(20)
  )

interval = 5
target_fps = 30

async def do_things():

  reg = InstructionRegistry()

  reg["rwheel"] = RegistryInstructionMetadata(
    rainbow_wheel_instr,
    [float]
  )
  reg["clear"] = RegistryInstructionMetadata(clear)
  reg["fill"] = RegistryInstructionMetadata(
    fill,
    [color_from_hex]
  )

  (run_loop, event) = create_instruction_loop(reg, app_context)

  asyncio.ensure_future(run_loop())

  def parse_params(parsers: list[ParseFunc]):
    return [get_parse_type_name(p) for p in parsers]

  def do_returnables(req: BeamRequest):
    # TODO review if we even need "!" now that protocols are split
    if not req.command.startswith("!"):
      raise BeamException(0x11)
    
    match req.command[1:]:
      case "list_instructions":
        return [{'id': x[0], 'param_types': parse_params(x[1].param_parsers)} for x in reg.items()]

  def handle_instructions(reqs: list[BeamRequest]) -> Result:
    event.setWithValue(reqs[-1:][0])

  server = await create_beam_server(
    DfpProtocolHandler(do_returnables),
    PfpProtocolHandler(handle_instructions)
  )

  boot_sequence.run(app_context.display, interval)

  async with server:
    await server.serve_forever()

if __name__ == "__main__":
  loop.run_until_complete(do_things())