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
  
interval = 20
target_fps = 30

def wheel(pos):
  return tuple(int(x * 255) for x in hsv_to_rgb(pos, 1.0, 1.0))
 
def do_render():
  pos = time.perf_counter() % interval

  for i in range(display.length):
    t = ((i / display.length) * interval + pos) % interval / interval
    display.setPixel(i, Color(wheel(t)))
  
  display.render()

  counter_thread.inc_count()

if __name__ == "__main__":
  display = PixelGuiDisplay(20)

  counter_thread = FrameCounterThread(do_total=True)
  counter_thread.start()

  frame_clock = FramerateRectifier()
  frame_clock.target_fps = target_fps

  while True:
    do_render()
    frame_clock.tick()
