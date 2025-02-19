import asyncio
from dataclasses import dataclass, field
from time import ctime
from typing import Any, Callable, Concatenate, Coroutine
from lux_core.color import Color
from lux_core.context import LuxContext
from lux_core.iris.instruction_parser import ParseFunc

@dataclass
class TickData():
  time: float
  """Where the pixel is located in a space from 0 to 1, typical the index normalized on total length"""
  pos: float

TimeColorFunction = Callable[Concatenate[TickData, ...], Color]
RegistryFunction = Callable[Concatenate[LuxContext, ...], Coroutine[Any, Any, None]]

@dataclass
class RegistryInstructionMetadata:
  func: RegistryFunction
  # TODO review, not sure that this feels correct, should parsers be set at start?
  param_parsers: list[ParseFunc] = field(default_factory=lambda: [])

class InstructionRegistry(dict[str, RegistryInstructionMetadata]):
  """
  Used to store how instructions map to functionality.
  Given a key (instruction identifier), map to a something that is used by other parts of the app
  """