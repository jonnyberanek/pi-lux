from collections import namedtuple
from typing import NamedTuple, Tuple, Union

ColorVector = Tuple[int, int, int]

def clamp(value: int, lower: int, upper: int) -> int:
  return max(min(value, upper), lower)

class Color(namedtuple('Color', 'r g b'), ColorVector):
  """
  Safe and easy color tuple with extra featuring
  """
  
  r: int
  g: int
  b: int

  def __new__(cls, rOrVector: Union[int, ColorVector],g=0,b=0, safe=True):
    # Define closure for conditional clamping
    condClamp = lambda c : c if not safe else Color.clampColor(c)

    # print(hex(rOrVector), hex(g), hex(b))

    # Converts any other list or tuple
    if(isinstance(rOrVector, list) or isinstance(rOrVector, tuple)):
      return super().__new__(cls, *condClamp(rOrVector))

    # New from expected r,b,g inputs
    return super().__new__(cls, *condClamp([rOrVector,g,b]))

  @staticmethod
  def clampColorInt(value): 
    return clamp(value, 0, 255)

  @staticmethod
  def clampColor(color):
    return map(Color.clampColorInt, color)
  
  @staticmethod
  def fromHexString(h: str):
    hi = int(h, 16)
    print(hex(hi))
    return Color(rOrVector= hi >> 16 & 0xFF, g = hi >> 8 & 0xFF, b = hi & 0xFF)

  def toHex(self, prefix="#"):
    return f'{prefix}%02x%02x%02x' % self
  

def rgb_to_rbg(color: Color) -> ColorVector: 
  return ColorVector(color.r, color.b. color.g)