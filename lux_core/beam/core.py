from asyncio import Protocol
from ctypes import c_ubyte
from dataclasses import dataclass, field
from typing import Any

@dataclass
class Instruction():
  id: str
  parameters: list[Any] = field(default_factory=lambda: [])

@dataclass
class BeamRequest():
  command: str
  parameters: list[str] = field(default_factory=lambda: [])

@dataclass
class RawInstruction(BeamRequest):
  command: str
  parameters: list[str] = field(default_factory=lambda: [])

"""
0x: OK
0x1 - 0xF: reserved for other OK expected states
0x10 - 0x1F: Common client error states
0x20 - 0x2F: Common server error states
"""

class BeamException(Exception):
  
  def __init__(self, code: int, *args):
    self.code = c_ubyte(code)
    super().__init__(*args)


def res_code(code: c_ubyte | int):
  return (code if isinstance(code, int) else code.value).to_bytes(1, 'big')