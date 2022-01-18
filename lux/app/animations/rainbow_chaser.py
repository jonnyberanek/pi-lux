from lux.core.strip import PixelDisplayWriter

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
def rainbowChaser():
  def gen(writer: PixelDisplayWriter):
    while True:
      for j in range(256):  # one cycle of all 256 colors in the wheel
        for i in range(writer.display.numPixels):
          writer.display.setPixel(i, wheel(((i * 256 // writer.display.numPixels) + j) % 256))
        writer.display.show()
        yield
  return gen