from collections import namedtuple
from typing import Any, Iterable, List, NamedTuple, Tuple, Union

class Rbg(namedtuple('Rbg', 'r b g')):
  def toRgb(self):
    return Rgb(self.r, self.g, self.b)

class Rgb(namedtuple('Rgb', 'r g b')):
  def toRbg(self):
    return Rbg(self.r, self.b, self.g)

clamp = lambda value, lower, upper : max(min(value, upper), lower)

AnyColor = Union[Rgb, Rbg, List[int]]

class Pixel(Rbg):
  """
  Need a better naming convention but this is to bridge to confusion between
  the library using an RBG color system instead of RGB. Takes in basically 
  anything and outputs an RBG tuple. Assumes any input is RBG unless explicitly
  denotes as an Rgb named-tuple input.

  Also safens all colors by default to avoid erroring in invalid values. 
  """

  def __new__(cls, rOrRgb: Union[int, AnyColor],b=0,g=0, safe=True):
    # Define closure for conditional clamping
    condClamp = lambda c : c if not safe else Pixel.clampColor(c)

    # Converts RGB
    if(isinstance(rOrRgb, Rgb)):
      return super().__new__(cls, *condClamp(rOrRgb.toRbg()))
    # Converts any other list or tuple
    if(isinstance(rOrRgb, list) or isinstance(rOrRgb, tuple)):
      return super().__new__(cls, *condClamp(rOrRgb))

    # New from expected r,b,g inputs
    return super().__new__(cls, *condClamp([rOrRgb,g,b]))

  @staticmethod
  def clampColorInt(value): 
    return clamp(value, 0, 255)

  @staticmethod
  def clampColor(color):
    return map(Pixel.clampColorInt, color)
