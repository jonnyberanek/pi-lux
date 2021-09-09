from led_strip import WS2801Strip, MirroredWS2801Strip
from pixlr.strip import PixelStripWriter
import board
from adafruit_ws2801 import WS2801

odata = board.MOSI
oclock = board.SCLK
numleds = 112
bright = 1.0

def getAppPixelWriter():
  return PixelStripWriter(
    MirroredWS2801Strip(oclock, odata, numleds, brightness=bright, auto_write=False)
  )