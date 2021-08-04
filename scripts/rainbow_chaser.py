import time
import random
import board
import adafruit_ws2801

# Set up board and leds
odata = board.MOSI
oclock = board.SCLK
numleds = 160
bright = 1.0
leds = adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
)

######################### HELPERS ##############################

# a random color 0 -> 224
def random_color():
    return random.randrange(0, 7) * 32

def wheel(pos):
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3)

# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle(leds, wait=0):
  for j in range(256):  # one cycle of all 256 colors in the wheel
    for i in range(160):
      leds[i] = wheel(((i * 256 // 160) + j) % 256)
    leds.show()

######################### MAIN LOOP ##############################
n_leds = len(leds)

while True:
	rainbow_cycle(leds)
