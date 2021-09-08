from led_strip import WS2801Strip
from pixlr.strip import PixelStripWriter
import board
from adafruit_ws2801 import WS2801

odata = board.MOSI
oclock = board.SCLK
numleds = 160
bright = 1.0

def getAppPixelWriter():
  return PixelStripWriter(
    WS2801Strip(oclock, odata, numleds, brightness=bright, auto_write=False)
  )