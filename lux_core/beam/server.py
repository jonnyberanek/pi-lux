import asyncio
from ctypes import c_ubyte
import socket
from typing import Callable
import websockets
import websockets.asyncio
import websockets.asyncio.server

from lux_core.beam.core import BeamException, Instruction, RawInstruction
from lux_core.logging import init_logging, get_logger

def parse_data(data: str) -> list[RawInstruction]:
  """
  Parses data and returns the list of instructions.
  
  Despite this, internally this is optimzed only parse the last instruction in
  the packet, since we'll discard out-of-date instructions anyways. Convention
  is kept for the sake of expandability in the future.
  """
  print(data)
  print([i for i in data.strip().rstrip(";;").split(";;")])
  return [parse_instruction([i for i in data.strip().rstrip(";;").split(";;")][-1])]

def parse_instruction(text: str):
  print(text)
  text = text.strip().rstrip(";")
  print(text)
  if len(text) == 0:
    raise ValueError("Instruction cannot be empty")
  command, *parameters = text.split(":", 1)
  return RawInstruction(command, [] if len(parameters) == 0 else parameters[0].split(";"))

def res_code(b: c_ubyte | int):
  return int(b).to_bytes(1, 'big')

logger = get_logger("beam_server")

type OnInstructionParsedHandler = Callable[[list[RawInstruction]], None]

def create_beam_handler(on_instructions_parsed: OnInstructionParsedHandler):

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
port = 4061

# HACK Will fix, but theoretically would never be problematic
server_ready_event = asyncio.Event()

async def create_beam_server(handle_instructions: OnInstructionParsedHandler):

  async def handler(websocket: websockets.ServerConnection):
    async for message in websocket:
        try:
          logger.debug(f"received {message!r}")
          handle_instructions(parse_data(message))
          await websocket.send("")
        except websockets.exceptions.ConnectionClosedOK:
          pass

  # handler = create_beam_handler(handle_instructions)

  # server =  await asyncio.start_server(handler, ip, port)
  server = await websockets.asyncio.server.serve(handler, ip, port)

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  logger.info(f'Listening on on {s.getsockname()[0]}:{port}')
  s.close()

  return server


async def main():

  # async with websockets.asyncio.server.serve(handler, "localhost", port):
  #       print(f"WebSocket server started on ws://{ip}:{port}")
  #       await asyncio.Future()  # Run forever


  async with await create_beam_server(lambda i: None) as server:
    await server.serve_forever()

if __name__ == "__main__":
  init_logging()
  asyncio.run(main())