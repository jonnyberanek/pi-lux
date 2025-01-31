import ctypes
from dataclasses import dataclass, field

@dataclass
class Instruction:
  id: str
  parameters: list[any] = field(default_factory=lambda: [])

class BeamException(Exception):
  
  def __init__(self, code: ctypes.c_ubyte, *args):
    self.code = code
    super().__init__(*args)