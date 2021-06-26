from smartStrip import SmartStrip
import time

FRAME_DUR = 0.05

pattern = [
	0x110000,
	0xff0000,
	0x800000,
	0x110000,
	0x040000,
	0x010001,
	0x000001,
	0x0000ff,
	0x000080,
	0x000011,
	0x000004,
	0x010001
]

def christmas(pixels):
	for i in range(0, len(pixels)):
		for led in range(0, len(pixels)):
			pos = (i+led)%len(pattern)
			pixels[led] = pattern[pos]
		pixels.show()
		time.sleep(FRAME_DUR)

def run(count):
	strip = SmartStrip()
	for x in range(0, count):
		christmas(strip.pixels)

