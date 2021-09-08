from pixlr.pixel import Rbg, Rgb
import time

import pixel_impl as impl
from pixlr.strip import PixelStripWriter

leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LinearConsoleDisplay()))
# leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LoopedConsoleDisplay()))
# leds = PixelStripWriter(impl.LoopConsiderateConsoleStrip(11))
while True: 
  for i in range(0,leds.strip.numPixels):
    leds.setPixels([0,1,0])
    leds.strip.setPixel(i, Rbg(255,500,22))
    leds.strip.show()
    time.sleep(0.2)

# from pixlr.pixel import Pixel, Rgb, Rbg

# colorRgb = Rgb(1,2,3)
# colorPixel = Pixel(1,3,2)

# print(isinstance(colorRgb, Rgb))
# print(isinstance(colorRgb, Rbg))
# print(isinstance(colorPixel, Rgb))
# print(isinstance(colorPixel, Rbg))

# color = Pixel(Rgb(0,33,55))
# print(color)
