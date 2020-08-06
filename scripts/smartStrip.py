from stripConfig import init
import time

def safeColor(val):
  return min(max(0,int(val)),255)
  
def lerp(v0, v1, t):
  return (1 - t) * v0 + t * v1;

def warmthToRBG(warmth):
  b = 214/4100 * warmth - 59
  g = 108/4100 * warmth + 96
  print(safeColor(b))
  print(safeColor(g))
  return (255, safeColor(b), safeColor(g)) 

class SmartStrip:
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