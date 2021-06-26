# wheel.py
# gradient.py
import time
from smartStrip import SmartStrip

def lerp(i, f, t):
  return i + (f-i) * t

def lerpi(i,f,t):
  return int(lerp(i,f,t))

def lerpColor(i, f, t):
  return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))

# frequency is leds per 
def colorLoop(colors, ledsPerColor=10, frequency=2):
  strip = SmartStrip()
  color = colors[0]
  numColors = len(colors)
  stripLength = len(strip.pixels)
  # create Lerp loop
  loop = []
  sequenceLength = numColors * ledsPerColor
  for i in range(stripLength):
    sequenceOffset = ((i) / ledsPerColor) % numColors
    colorIndex = int(sequenceOffset)
    color = lerpColor(colors[colorIndex], colors[(colorIndex+1) % numColors], sequenceOffset % 1)
    loop.append(color)
  strip.pixels.show()
  
  while True:
    for j in range(stripLength):
      for i in range(stripLength):
        strip.pixels[i] = loop[int(j+i) % stripLength]   
        # index = int(pos)  # Integer which defines the index relative to time
        # t = pos-index # Float 0 <= x < 1 - defines position of lerp for current index
      #print(strip.pixels[0])
      strip.pixels.show()
      time.sleep(1.0/frequency)

colorLoop([(0,207,169), (196,154, 0)], 50, 10)
