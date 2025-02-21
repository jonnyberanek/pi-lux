import asyncio

from websockets import connect 
from lux_core.beam.core import Instruction

def instruction_to_bytes(instruction: Instruction) -> bytes:
  string = instruction.id
  if len(instruction.parameters) > 0:
    ps = ";".join([str(p) for p in instruction.parameters])
    string += ":" + ps + ";;"
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

# async def main():
#   async with BeamClient(('localhost', 8888)) as client:
#     print(await client.send_instruction(Instruction('fill', ['ff00ff'])))
#     print(await client.send_instruction(Instruction('fill', ['ffff00'])))

# if __name__ == "__main__":
#   asyncio.run(main())

async def hello():
    async with connect("ws://localhost:8888") as websocket:
        await websocket.send("fill:00ff00;;")
        message = await websocket.recv()
        print(message)

        await websocket.send("fill:00ff00;;")
        await websocket.send("fill:00fff0;;")
        message = await websocket.recv()
        print(message)


if __name__ == "__main__":
    asyncio.run(hello())