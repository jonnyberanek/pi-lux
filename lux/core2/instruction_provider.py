
from abc import ABC, abstractmethod
from typing import Union

from lux.core2.main import Instruction

class InstructionProvider(ABC):
  STOP = "STOP"

  @abstractmethod
  def consumeInstruction(self) -> Union[Instruction, str, None]:
    pass
  
  @abstractmethod
  def addInstruction(self, instruction: Instruction):
    pass