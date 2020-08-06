import board
import adafruit_ws2801

odata = board.MOSI
oclock = board.SCLK
numleds = 160
bright = 1.0

### Example for a Feather M4 driving 25 12mm leds
def init():
  return adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
  )
