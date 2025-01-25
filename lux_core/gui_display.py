import asyncio
from threading import Thread
import threading
import time
from colorsys import hsv_to_rgb
from lux_core.diag.frame_counting import FrameCounterThread
from lux_core.nonopt.framerate_rectifier import FramerateRectifier

from lux_core.color import Color
from lux_core.display import Display
from lux_core.pixel_gui import DEFAULT_PIXEL_SIZE, PixelRowGui

class PixelGuiDisplay(Display):

  def __init__(self, pixelsPerRow: int, rows=1) -> None:
    super().__init__()
    self.__numPixels = pixelsPerRow*rows
    self.gui = PixelRowGui(DEFAULT_PIXEL_SIZE, pixelsPerRow, rows)

  def setPixel(self, index: int, color: Color):
    self.gui.setPixel(index, color)
  
  def render(self):
    self.gui.window.update()

  @property
  def length(self) -> int:
    return self.__numPixels
  
interval = 5
target_fps = 30

def hue_to_color(h):
  return Color(tuple(int(x * 255) for x in hsv_to_rgb(h, 1.0, 1.0)))
 
def do_render_1(display: Display):
  pos = time.perf_counter() % interval

  for i in range(display.length):
    t = ((i / display.length) * interval + pos) % interval / interval
    display.setPixel(i, hue_to_color(t))
  
  display.render()

def do_render_2(display: Display):
  pos = time.perf_counter() % interval

  for i in range(display.length):
    t = pos / interval
    display.setPixel(i, hue_to_color(t))
  
  display.render()

class RenderThread(Thread):

  should_render = threading.Event()

  def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = True
    self.render_fn = None
    self.event = threading.Event()

  def run(self):
    display = PixelGuiDisplay(20)

    counter_thread = FrameCounterThread(do_total=True)
    counter_thread.start()

    frame_clock = FramerateRectifier()
    frame_clock.target_fps = target_fps
    
    while self.should_render():
      if self.render_fn is not None:
        self.render_fn(display)
      counter_thread.inc_count()
      frame_clock.tick()

class PseudoCommandThread(Thread):

  def __init__(self, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.daemon = False
    self.render_fn = None
  
  def run(self):
    time.sleep(3)

def boot_sequence(display: Display):

  def render(t):
    pos = int(t % 2)

    for i in range(display.length):
      value = (i + pos) % 2 * 255

      print(value)
      display.setPixel(i, Color(value, value, value))
    
    display.render()

  def render2(t):
    fade = max(0, -(2 - t) ** 2 + 4) / 4
    print(fade)
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

      
    # counter_thread.inc_count()

async def waiter(event):
    print('waiting for it ...')
    await event.wait()
    print('... got it!')

async def main():
    # loop = asyncio.new_event_loop()

    # loop.run_forever()
    # Create an Event object.
    event = asyncio.Event()

    # Spawn a Task to wait until 'event' is set.
    waiter_task = asyncio.create_task(waiter(event))

    # Sleep for 1 second and set the event.
    await asyncio.sleep(1)
    event.set()

    # Wait until the waiter task is finished.
    await waiter_task

if __name__ == "__main__":
  # asyncio.run(main())
  PixelGuiDisplay(20)
  time.sleep(23)
  # boot_sequence(PixelGuiDisplay(20))
  