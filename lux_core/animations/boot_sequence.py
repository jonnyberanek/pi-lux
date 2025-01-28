from colorsys import hsv_to_rgb
import time

from lux_core.color import Color
from lux_core.display import Display

def run(display: Display, interval: int):

  def render(t):
    pos = int(t % 2)

    for i in range(display.length):
      value = (i + pos) % 2 * 255

      display.setPixel(i, Color(value, value, value))
    
    display.render()

  def render2(t):
    fade = max(0, -(2 - t) ** 2 + 4) / 4
    pos = t % interval

    for i in range(display.length):
      h = ((i / display.length) * interval + pos) % interval / interval

      color = Color(tuple(int(x * 255) for x in hsv_to_rgb(h, 1.0, fade)))
      display.setPixel(i, color)
    
    display.render()
  
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
  while curr <= 4:
    render2(curr)
    curr = (time.perf_counter() - start) * 2
  
  for i in range(display.length):
    display.setPixel(i, Color(0,0,0))
  display.render()