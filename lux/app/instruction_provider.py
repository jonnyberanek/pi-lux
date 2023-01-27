from queue import Queue

from lux.core2.instruction_provider import InstructionProvider
from lux.core2.main import Instruction

class QueueInstructionProvider(InstructionProvider):

  def __init__(self, queue: Queue) -> None:
    super().__init__()
    self.queue = queue

  def consumeInstruction(self):
    lastInstruction = self.__getLast(self.queue)
    if lastInstruction == None:
      return None
    return lastInstruction
  
  def addInstruction(self, instruction: Instruction):
    self.queue.put(instruction)

  def __getLast(self, queue: Queue):
    last = None
    while not queue.empty():
      last = queue.get()
    return last
