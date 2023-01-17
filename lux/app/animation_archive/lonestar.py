from lux.core2.pixel import Rgb

def lonestar(writer):
  while True: 
    for i in range(0,writer.display.numPixels):
      writer.setPixels([0,0,0])
      writer.display.setPixel(i, Rgb(255,255,255))
      writer.display.show()
      yield