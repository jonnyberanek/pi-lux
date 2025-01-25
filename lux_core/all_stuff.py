import asyncio
from colorsys import hls_to_rgb, hsv_to_rgb
from dataclasses import dataclass
from threading import Thread
import threading
import time
from typing import TypeVar, Union
import logging

from lux_core.color import Color, rgb_to_rbg
from lux_core.display import Display
from lux_core.gui_display import PixelGuiDisplay
from lux_core.nonopt.framerate_rectifier import FramerateRectifier

VERBOSE = 5

logging.addLevelName(VERBOSE, "VERBOSE")

logger = logging.getLogger(__name__)
logging.basicConfig(level=VERBOSE)

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

  odata = board.MOSI
  oclock = board.SCLK
  numleds = 46
  bright = 1.0
  app_context.display = LinearWS2801Display(
      oclock, odata, numleds, brightness=bright, auto_write=False
  )
except Exception as e:
  logger.info("Failed to initialize physical display: %s", e)
  app_context.display = PixelGuiDisplay(20)

class ADataEvent(asyncio.Event):
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
  
aevent = ADataEvent()

async def listen_for_instructions():
  logger.debug("Ready to receive events...")
  while True:
    data = await aevent.waitForValue()
    c = Color.fromHexString(data.parameters[0])
    print(f"Event received with: {c.toHex()}")
    aevent.clear()

    display = app_context.display

    # c = Color.fromHexString(data.parameters[0])
    for i in range(display.length):
      display.setPixel(i, c)
    display.render()

interval = 5
target_fps = 30

def boot_sequence(display: Display):

  def render(t):
    pos = int(t % 2)

    for i in range(display.length):
      value = (i + pos) % 2 * 255

      # print(value)
      display.setPixel(i, Color(value, value, value))
    
    display.render()

  def render2(t):
    fade = max(0, -(2 - t) ** 2 + 4) / 4
    # print(fade)
    pos = t % interval

    for i in range(display.length):
      h = ((i / display.length) * interval + pos) % interval / interval

      color = Color(tuple(int(x * 255) for x in hsv_to_rgb(h, 1.0, fade)))
      display.setPixel(i, color)
    
    display.render()

  # counter_thread = FrameCounterThread(do_total=True)
  # counter_thread.start()

  frame_clock = FramerateRectifier()
  frame_clock.target_fps = target_fps
  
  # while True:
  #   # render()
  time.sleep(0.5)
  for i in range(0,2):
    render(i)
    time.sleep(0.15)
    for i in range(display.length):
      display.setPixel(i, Color(0,0,0))
    display.render()
    time.sleep(0.15)
  time.sleep(0.5)
  
  start = time.perf_counter()
  curr = 0.0
  print(start)
  while curr <= 4:
    render2(curr)
    curr = (time.perf_counter() - start) * 2

  
  for i in range(display.length):
    display.setPixel(i, Color(0,0,0))
  display.render()

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Protocol

@dataclass
class Instruction:
  command: str
  parameters: list[any]

UTF8 = "utf-8"

def parse_data(data: str) -> list[Instruction]:
  """
  Parses data and returns the list of instructions.
  
  Despite this, internally this is optimzed only parse the last instruction in
  the packet, since we'll discard out-of-date instructions anyways. Convention
  is kept for the sake of expandability in the future.
  """
  return [parse_instruction(i) for i in data.strip().rstrip(";;").split(";;")[-1:]]

def parse_instruction(text: str):
  text = text.strip().rstrip(";")
  if len(text) == 0:
    raise ValueError("Instruction cannot be empty")
  command, *parameters = text.split(":", 1)
  return Instruction(command, [] if len(parameters) == 0 else parameters[0].split(";"))

def res_code(b: int):
  return b.to_bytes(1, 'big')

class InstructionProtocol(Protocol):
  def connectionMade(self):
    logger.info(f"Connected to {self.transport.getPeer().host}")

  def dataReceived(self, data):
    logger.debug(f"{self.transport.getPeer().host} sent \"{data}\"")
    
    try:
      instr, = parse_data(data.decode(UTF8))
      logger.debug(f"Sending instruction {instr}")
      aevent.setWithValue(instr)
    except Exception:
      print("oh no")
    self.transport.write(res_code(0xFA))


class InstructionFactory(Factory):
  def buildProtocol(self, addr):
    return InstructionProtocol()

def run_instruction_server():
  endpoint = TCP4ServerEndpoint(reactor, 8888)
  endpoint.listen(InstructionFactory())
  print("listening on 8888")
  reactor.run()

# ev = asyncio.Event()
async def run_commands():
  while True:
    y = hsv_to_rgb(time.time() % 1, 1.0, 1.0)

    c = [int(x * 255) for x in y]

    aevent.setWithValue(Instruction("hello", [f"{c[0]:02x}{c[1]:02x}{c[2]:02x}"]))
    await asyncio.sleep(0.001)

async def do_things():
  asyncio.ensure_future(listen_for_instructions())

  boot_sequence(app_context.display)

  while True:
    await asyncio.sleep(0.01)
  
def start_instruction_socket_server():
  endpoint = TCP4ServerEndpoint(reactor, 8888)
  endpoint.listen(InstructionFactory())
  print("listening on 8888")
  Thread(daemon=True, target=reactor.run, args=(False,)).start()

if __name__ == "__main__":
  loop.run_until_complete(do_things())