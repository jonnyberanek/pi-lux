from animations.rainbow import randomRainbowFade
from pixlr.animation import Animator
from pixlr.pixel import Rgb
import console_pixel_impls as impl
from pixlr.strip import PixelStripWriter
# from led_strip_impl import getAppPixelWriter

"""
Lerp Helpers
"""
def lerp(i, f, t):
  return i + (f-i) * t

def lerpi(i,f,t):
  return int(lerp(i,f,t))

def lerpColor(i, f, t):
  return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))

def lonestar(writer: PixelStripWriter):
  while True: 
    for i in range(0,writer.strip.numPixels):
      writer.setPixels([0,0,0])
      writer.strip.setPixel(i, Rgb(900,555,555))
      writer.strip.show()
      yield

def colorLoop(colors, ledsPerColor=10):
  def gen(writer):
    color = colors[0]
    numColors = len(colors)
    stripLength = writer.strip.numPixels
    # create Lerp loop
    loop = []
    for i in range(stripLength):
      sequenceOffset = ((i) / ledsPerColor) % numColors
      colorIndex = int(sequenceOffset)
      color = lerpColor(colors[colorIndex], colors[(colorIndex+1) % numColors], sequenceOffset % 1)
      loop.append(color)
    writer.strip.show()
    while True:
      for j in range(stripLength):
        for i in range(stripLength):
          writer.strip.setPixel(i, loop[int(j+i) % stripLength])
          # index = int(pos)  # Integer which defines the index relative to time
          # t = pos-index # Float 0 <= x < 1 - defines position of lerp for current index
        #print(strip.pixels[0])
        writer.strip.show()
        yield
  return gen

def main():
  # leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LinearConsoleDisplay()))
  leds = PixelStripWriter(impl.ConsoleStrip(20, impl.LoopedConsoleDisplay()))
  # leds = PixelStripWriter(impl.LoopConsiderateConsoleStrip(10))
  # leds = getAppPixelWriter()
  animator = Animator(leds, frequency=30)
  animator.startAnimation(randomRainbowFade(30))

main()