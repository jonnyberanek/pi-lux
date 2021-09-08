from collections import namedtuple
from typing import Any, Iterable, NamedTuple, Tuple

class Rbg(namedtuple('Rbg', 'r b g')):
  def toRgb(self):
    return Rgb(self.r, self.g, self.b)

class Rgb(namedtuple('Rgb', 'r g b')):
  def toRbg(self):
    return Rbg(self.r, self.b, self.g)

clamp = lambda value, lower, upper : max(min(value, upper), lower)

class Pixel(Rbg):

  def __new__(cls, rOrRgb,b=0,g=0, safe=True):
    condClamp = lambda c : c if not safe else Pixel.clampColor(c)

    if(isinstance(rOrRgb, Rgb)):
        return super().__new__(cls, *condClamp(rOrRgb.toRbg()))

    return super().__new__(cls, *condClamp([rOrRgb,g,b]))

  @staticmethod
  def clampColorInt(value): 
    return clamp(value, 0, 255)

  @staticmethod
  def clampColor(color):
    return map(Pixel.clampColorInt, color)
