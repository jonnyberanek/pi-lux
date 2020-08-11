# gradient.py
import time
from smartStrip import SmartStrip

def lerp(i, f, t):
    return i + (f-i) * t

def lerpi(i,f,t):
    return int(lerp(i,f,t))

def lerpColor(i, f, t):
    return (lerpi(i[0], f[0], t), lerpi(i[1], f[1], t), lerpi(i[2], f[2], t))

def colorLoop(colors, interval=3):
    strip = SmartStrip()
    color = colors[0]
    numColors = len(colors)
    while True:
        pos =  (time.time() / interval) % numColors
        index = int(pos)  # Integer which defines the index relative to time
        t = pos-index # Float 0 <= x < 1 - defines position of lerp for current index
        color = lerpColor(colors[index], colors[(index+1) % numColors], t)
        strip.fill(color)
        time.sleep(0.02)

colorLoop([(160,255,160), (160,160,255), (255,160,160)], 2)
