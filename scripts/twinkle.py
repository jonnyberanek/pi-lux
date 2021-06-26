from smartStrip import SmartStrip
import time

FRAME_SEC = 1/60

class Twinkle():
	def __init__(self):
		self.strip = SmartStrip()
		#print(dir(self.strip))
		self.strip.fill((255,255,255))
		#self.fadeValue = [1] * len(self.strip.pixels)

	def run(self):
		while(True):
			self.update()
			self.strip.pixels.show()
			time.sleep(FRAME_SEC)

	def update(self):
		for led in range(0, len(self.strip.pixels)):
			self.strip.pixels[led] = (self.strip.pixels[led][0]-1,self.strip.pixels[led][1]-1,self.strip.pixels[led][2]-1)

Twinkle().run()
