from lux.core2.main import Display

def getAppPixelDisplay() -> Display:
  try:
    import board

    from lux.app.display.displays.led_displays import MirroredWS2801Display, LinearWS2801Display
    odata = board.MOSI
    oclock = board.SCLK
    numleds = 112
    bright = 1.0
    return MirroredWS2801Display(
      oclock, odata, numleds, brightness=bright, auto_write=False
    )
  except:
    from lux.app.display.displays.gui_display import PixelGuiDisplay
    return PixelGuiDisplay(pixelsPerRow=20, rows=1)
  
