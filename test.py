from pixlr.pixel import Rbg, Rgb
import time

import console_pixel_impls as impl
from pixlr.strip import PixelStripWriter
from led_strip_impl import getAppPixelWriter

# leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LinearConsoleDisplay()))
# leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LoopedConsoleDisplay()))
# leds = PixelStripWriter(impl.LoopConsiderateConsoleStrip(11))
leds = getAppPixelWriter()
while True: 
  for i in range(0,leds.strip.numPixels):
    leds.setPixels([0,0,0])
    leds.strip.setPixel(i, Rgb(900,555,555))
    leds.strip.show()
    time.sleep(0.05)

# from pixlr.pixel import Pixel, Rgb, Rbg

# colorRgb = Rgb(1,2,3)
# colorPixel = Pixel(1,3,2)

# print(isinstance(colorRgb, Rgb))
# print(isinstance(colorRgb, Rbg))
# print(isinstance(colorPixel, Rgb))
# print(isinstance(colorPixel, Rbg))

# color = Pixel(Rgb(0,33,55))
# print(color)
