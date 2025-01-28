import asyncio 
from lux_core.beam.core import Instruction

def instruction_to_bytes(instruction: Instruction) -> str:
  string = instruction.command
  if len(instruction.parameters) > 0:
    string += ":" + ";".join(instruction.parameters) + ";;"
  return string.encode()
    
class BeamClient:
  def __init__(self, conn: tuple[str, int]):
    self.conn = conn

  async def __aenter__(self):
    self.reader, self.writer = await asyncio.open_connection(*self.conn)
    return self
  
  async def __aexit__(self, exc_type, exc_val, exc_tb):
    self.writer.close()
    await self.writer.wait_closed()

  async def send_instruction(self, instr: Instruction):
    self.writer.write(instruction_to_bytes(instr))
    await self.writer.drain()
    return await self.reader.read(1)

async def main():
  async with BeamClient(('localhost', 8888)) as client:
    print(await client.send_instruction(Instruction('fill', ['ff00ff'])))
    print(await client.send_instruction(Instruction('fill', ['ffff00'])))

if __name__ == "__main__":
  asyncio.run(main())