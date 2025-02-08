from asyncio import Protocol
import ctypes
from dataclasses import dataclass, field
from typing import Any

@dataclass
class InstructionProto(Protocol):
  id: str
  parameters: list[Any]

@dataclass
class Instruction:
  id: str
  parameters: list[Any] = field(default_factory=lambda: [])

@dataclass
class RawInstruction():
  id: str
  parameters: list[str] = field(default_factory=lambda: [])

class BeamException(Exception):
  
  def __init__(self, code: ctypes.c_ubyte, *args):
    self.code = code
    super().__init__(*args)