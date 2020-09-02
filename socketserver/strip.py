import board
import adafruit_ws2801
import time

odata = board.MOSI
oclock = board.SCLK
numleds = 160
bright = 1.0

### Example for a Feather M4 driving 25 12mm leds
def init():
  return adafruit_ws2801.WS2801(
    oclock, odata, numleds, brightness=bright, auto_write=False
  )


BRIGHT_MAX = 255.0
BRIGHT_MOD = 118.0

def toneDown(bit, warmth):
  return bit - ((1 - bit/BRIGHT_MAX * (warmth-1900)/4100.0) * BRIGHT_MOD)

def safeColor(val):
  return min(max(0,int(val)),255)
  
def lerp(v0, v1, t):
  return (1 - t) * v0 + t * v1;

def warmthToRBG(warmth):
  print(type(warmth))
  b = toneDown(214/4100 * warmth - 59.0, warmth)
  g = toneDown(108/4100 * warmth + 95.0, warmth)
  print(safeColor(b))
  print(safeColor(g))
  return (safeColor(toneDown(255, warmth)), safeColor(b), safeColor(g))

class Strip:
  def __init__(self):
    self.pixels = init()
  
  def clear(self):
    self.pixels.fill((0,0,0))
    self.pixels.show()
  
  def fill(self, color):
    self.pixels.fill(color)
    self.pixels.show()
    
  def fillWarmth(self, warmth):
    self.pixels.fill(warmthToRBG(warmth))
    self.pixels.show()
    
  def lerpToFill(self, color):
    start = time.time()
    startColor = self.pixels[0]
    while(time.time() - start <= 1):
      r = safeColor(lerp(startColor[0], color[0], time.time() - start) )
      b = safeColor(lerp(startColor[1], color[1], time.time() - start) )
      g = safeColor(lerp(startColor[2], color[2], time.time() - start) )
      self.fill((r,b,g)) 
      time.sleep(0.01)
    self.fill(color)
