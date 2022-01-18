from lux.core.strip import IPixelList, PixelDisplayWriter


def getAppPixelWriter() -> PixelDisplayWriter:
  strip: IPixelList = None
  try:
    import board
    from lux.app.display_lists import MirroredWS2801Strip, WS2801Strip
    odata = board.MOSI
    oclock = board.SCLK
    numleds = 112
    bright = 1.0
    MirroredWS2801Strip(
      oclock, odata, numleds, brightness=bright, auto_write=False
    )
  except:
    pass
  if(strip == None):
    from lux.app.display_lists.gui import PixelGuiDisplay
    strip = PixelGuiDisplay(numPixels=40)
  return PixelDisplayWriter(strip)
