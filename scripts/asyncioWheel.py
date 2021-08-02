# wheel.py
# gradient.py
import time
import asyncio
from smartStrip import SmartStrip

"""
Lerp Helpers
"""
def lerp(i, f, t):
  return i + (f-i) * t

def lerpi(i,f,t):
  return int(lerp(i,f,t))

def lerpColor(i, f, t):
  return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))


"""
Task
"""
# frequency is leds per 
async def colorLoop(colors, ledsPerColor=10, frequency=2):
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

"""
Asyncio Event setup
"""
loop = asyncio.get_event_loop()
try:
  asyncio.ensure_future(colorLoop([(0,207,169), (196,154, 0)], 50, 10))
  # asyncio.ensure_future(colorLoop([(255,0,0), (0,255,0), (0,0,255)], 50, 10))
  loop.run_forever()
except KeyboardInterrupt:
  pass
finally:
  print('Closing')
  loop.close()


