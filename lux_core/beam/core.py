import ctypes
from dataclasses import dataclass

@dataclass
class Instruction:
  command: str
  parameters: list[any]

class BeamException(Exception):
  
  def __init__(self, code: ctypes.c_ubyte, *args):
    self.code = code
    super().__init__(*args)