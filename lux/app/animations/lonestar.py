from lux.core.pixel import Rgb
from lux.core.strip import PixelDisplayWriter

def lonestar(writer: PixelDisplayWriter):
  while True: 
    for i in range(0,writer.display.numPixels):
      writer.setPixels([0,0,0])
      writer.display.setPixel(i, Rgb(255,255,255))
      writer.display.show()
      yield