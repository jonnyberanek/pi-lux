from ledcontroller.strip import IPixelList, PixelDisplayWriter

def getAppPixelWriter() -> PixelDisplayWriter:
  strip: IPixelList = None
  try:
    import board
    from adafruit_ws2801 import WS2801
    from led_strip import MirroredWS2801Strip, WS2801Strip
    odata = board.MOSI
    oclock = board.SCLK
    numleds = 112
    bright = 1.0
    strip = MirroredWS2801Strip(
      oclock, odata, numleds, brightness=bright, auto_write=False
    )
  except:
    pass
  if(strip == None):
    from gui_pixel_impls import PixelGuiDisplay
    strip = PixelGuiDisplay(numPixels=40)
  return PixelDisplayWriter(strip)
