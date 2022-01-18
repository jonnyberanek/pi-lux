from lux.core.strip import PixelDisplayWriter

from .helpers import lerpColor


def colorLoop(colors, ledsPerColor=10):
  def gen(writer: PixelDisplayWriter):
    color = colors[0]
    numColors = len(colors)
    stripLength = writer.strip.numPixels
    # create Lerp loop
    loop = []
    for i in range(stripLength):
      sequenceOffset = ((i) / ledsPerColor) % numColors
      colorIndex = int(sequenceOffset)
      color = lerpColor(colors[colorIndex], colors[(colorIndex+1) % numColors], sequenceOffset % 1)
      loop.append(color)
    writer.strip.show()
    while True:
      for j in range(stripLength):
        for i in range(stripLength):
          writer.strip.setPixel(i, loop[int(j+i) % stripLength])
          # index = int(pos)  # Integer which defines the index relative to time
          # t = pos-index # Float 0 <= x < 1 - defines position of lerp for current index
        #print(strip.pixels[0])
        writer.strip.show()
        yield
  return gen
