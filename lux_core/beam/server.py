import asyncio
from ctypes import c_ubyte
import itertools
import json
import socket
from typing import Any, Callable, Sequence
import websockets
import websockets.asyncio
import websockets.asyncio.server

from lux_core.beam.core import BeamException, Instruction, RawInstruction, BeamRequest, res_code
from lux_core.beam.protocols.dfp_handler import DfpProtocolHandler
from lux_core.beam.protocols.handler import ProtocolHandler
from lux_core.beam.protocols.pfp_handler import PfpProtocolHandler
from lux_core.logger import VERBOSE, init_logging, get_logger

def parse_data(data: str) -> list[BeamRequest]:
  """
  Parses data and returns the list of instructions.
  
  Despite this, internally this is optimzed only parse the last instruction in
  the packet, since we'll discard out-of-date instructions anyways. May replace
  but convention is intended for expandability in the future.
  """
  return [parse_instruction([i for i in data.strip().rstrip(";;").split(";;")][-1])]

def parse_instruction(text: str):
  text = text.strip().rstrip(";")
  if len(text) == 0:
    raise ValueError("Instruction cannot be empty")
  command, *parameters = text.split(":", 1)
  return BeamRequest(command, [] if len(parameters) == 0 else parameters[0].split(";"))



logger = get_logger("beam_server")

type Result = Any
type OnRequestParsedHandler = Callable[[list[BeamRequest]], Result]

def create_beam_handler(on_instructions_parsed: OnRequestParsedHandler):

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

PFP = "pfp"
DFP = "dfp"

async def create_beam_server(
    dfp_handler: ProtocolHandler,
    pfp_handler: ProtocolHandler
):
  

  async def handler(websocket: websockets.ServerConnection):
    async for message in websocket:
        protocol_handler = dfp_handler if websocket.subprotocol == DFP else pfp_handler

        try:
          logger.debug(f"received {message!r} from {websocket.id}")
          requests = parse_data(str(message))

          logger.debug(f"handling {requests}")

          await websocket.send(protocol_handler.handle_requests(requests))
          # await websocket.send(res_code(0))
          # return

          # res = handle_instructions(parse_data(str(message)))

          # await websocket.send(str(res))
        except websockets.exceptions.ConnectionClosedOK:
          logger.debug("Connection closed by client")
        except BeamException as e:
          logger.info(f"BeamException: {e!r}")
          await websocket.send(protocol_handler.handle_exception(e))
          await websocket.close(1011)
        except Exception as e:
          logger.error(e, exc_info=True)
          await websocket.close(1011)

  # handler = create_beam_handler(handle_instructions)

  def select_subprotocol(connection: websockets.ServerConnection, subprotocols:  Sequence[websockets.Subprotocol]) -> websockets.Subprotocol | None:
    if 'dfp' in subprotocols:
      return DFP
    return PFP

  # server =  await asyncio.start_server(handler, ip, port)
  server = await websockets.asyncio.server.serve(handler, ip, port, select_subprotocol=select_subprotocol)

  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  s.connect(("8.8.8.8", 80))
  logger.info(f'Listening on on {s.getsockname()[0]}:{port}')
  s.close()

  return server


async def main():

  # async with websockets.asyncio.server.serve(handler, "localhost", port):
  #       print(f"WebSocket server started on ws://{ip}:{port}")
  #       await asyncio.Future()  # Run forever

  async with await create_beam_server(
    DfpProtocolHandler(lambda x: None),
    PfpProtocolHandler(lambda x: None)
  ) as server:
    await server.serve_forever()

if __name__ == "__main__":
  init_logging()
  asyncio.run(main())