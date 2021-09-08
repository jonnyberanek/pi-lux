# from pixlr.strip import PixelStripWriter
# import pixel_impl as impl
# from math import floor
# import time

# # leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LinearConsoleDisplay()))
# leds = PixelStripWriter(impl.ConsoleStrip(10, impl.LoopedConsoleDisplay()))
# while True: 
#   for i in range(0,leds.strip.numLeds):
#     leds.setPixels([0,0,0])
#     leds.strip.setPixel(i, [255,255,255])
#     leds.strip.show()
#     # leds.setPixels
#     time.sleep(0.33)

from pixlr.pixel import Pixel, Rgb, Rbg

colorRgb = Rgb(1,2,3)
colorPixel = Pixel(1,3,2)

print(isinstance(colorRgb, Rgb))
print(isinstance(colorRgb, Rbg))
print(isinstance(colorPixel, Rgb))
print(isinstance(colorPixel, Rbg))

color = Pixel(Rgb(0,33,55))
print(color)