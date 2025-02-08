import asyncio
from ctypes import c_ubyte
from typing import Callable

from lux_core.beam.core import BeamException, Instruction
from lux_core.logging import init_logging, get_logger

def parse_data(data: str) -> list[Instruction]:
  """
  Parses data and returns the list of instructions.
  
  Despite this, internally this is optimzed only parse the last instruction in
  the packet, since we'll discard out-of-date instructions anyways. Convention
  is kept for the sake of expandability in the future.
  """
  return [parse_instruction(i) for i in data.strip().rstrip(";;").split(";;")[-1:]]

def parse_instruction(text: str):
  text = text.strip().rstrip(";")
  if len(text) == 0:
    raise ValueError("Instruction cannot be empty")
  command, *parameters = text.split(":", 1)
  return Instruction(command, [] if len(parameters) == 0 else parameters[0].split(";"))

def res_code(b: c_ubyte | int):
  return int(b).to_bytes(1, 'big')

logger = get_logger("beam_server")

def create_beam_handler(on_instructions_parsed: Callable[[list[Instruction]], None]):

  async def handle(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peer = None
    try:
      while not reader.at_eof():
        data = await reader.readuntil(b";;")
        peer = writer.get_extra_info('peername')
        
        logger.debug(f"Received {data!r} from {peer!r}")

        on_instructions_parsed(parse_data(data.decode()))

        code = res_code(0x00)
        logger.debug(f"Sending success code: {code!r}")

        writer.write(code)
        await writer.drain()

    except BeamException as e:
      logger.info(f"BeamException: {e!r}")
      code = res_code(e.code)
      writer.write(code)
      await writer.drain()

    except asyncio.IncompleteReadError as e:
      logger.info(f"Incomplete read ({e.partial.decode()!r}), assuming closed.")

    except ConnectionResetError as e:
      logger.info(f"Connection closed by client ({peer!r})")

    except Exception as e:
      logger.error(e, exc_info=True)
      if not writer.is_closing():
        writer.write(res_code(0xFF))
        pass
    
    finally:
      if not writer.is_closing():
        logger.info(f"Closing connection... ({peer!r})")
        writer.close()
        await writer.wait_closed()

  return handle

ip = '0.0.0.0'
port = 8888

# HACK Will fix, but theoretically would never be problematic
server_ready_event = asyncio.Event()


async def create_beam_server(handle_instructions: Callable[[list[Instruction]], None]):
  handler = create_beam_handler(handle_instructions)

  server =  await asyncio.start_server(handler, ip, port)

  addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
  logger.info(f'Serving on {addrs}')

  return server

async def main():
  async with await create_beam_server(lambda i: None) as server:
    await server.serve_forever()

if __name__ == "__main__":
  init_logging()
  asyncio.run(main())