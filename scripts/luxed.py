import sys
import time
import random
import board
import adafruit_ws2801



#BRIGHT_MOD = min(max(0.2*(1-(sys.argv[1]-1900)/4100),0),1)

# Set up board and leds
odata = board.MOSI
oclock = board.SCLK
numleds = 160
bright = 1.00
leds = adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
)

def safeColor(val):
  return min(max(0,int(val)),255)

def warmthToRBG(warmth):
  b = 214/4100 * warmth - 59
  g = 108/4100 * warmth + 96
  print(safeColor(b))
  print(safeColor(g))
  return (255, safeColor(b), safeColor(g)) 

leds.fill(warmthToRBG(int(sys.argv[1])))
leds.show()