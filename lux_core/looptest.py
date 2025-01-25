
import asyncio
from dataclasses import dataclass
import socket
from threading import Thread
from time import sleep
from typing import Generic, TypeVar, Union

loop = asyncio.get_event_loop()
at_point = None

T = TypeVar("T")

class DataEvent(asyncio.Event):
  """
  This retains a value with an asynchronous event until it is cleared. This has
  the opportunity to drop events if "overwritten" by a subsequent `set` before
  it can be consumed. This is expected, this should be used in a realtime
  system, prefer `asyncio.Queue` otherwise.
  """
  data: Union[T | None] = None

  def setWithValue(self, value: T):
    self.data = value
    return self.set

  def clear(self):
    self.data = None
    return super().clear()
  
  async def waitForValue(self) -> T:
    await super().wait()
    return self.data
  
event = DataEvent()

async def main():
  while True:
    print("waiting for events")
    data = await event.waitForValue()
    print(f"we got it: {data}! (at {at_point})")
    await asyncio.sleep(1.0)
    event.clear()
    print("cleared")
  

class RunnerThread(Thread):

  def __init__(self, group = None, target = None, name = None, args = ..., kwargs = None, *, daemon = None):
    super().__init__(group, target, name, args, kwargs, daemon=True)

  def run(self):
    print("run")
    global at_point
    sleep(0.5)
    at_point = 1
    print("run")
    # loop.call_soon_threadsafe(event.set)
    loop.call_soon_threadsafe(event.setWithValue("123"))
    sleep(0.5)
    at_point = 2
    print("run")
    # loop.call_soon_threadsafe(event.set)
    loop.call_soon_threadsafe(event.setWithValue("234"))
    sleep(0.5)
    at_point = 3
    print("run")
    # loop.call_soon_threadsafe(event.set)
    loop.call_soon_threadsafe(event.setWithValue("345"))
    sleep(5)
    at_point = 4
    print("run")
    # loop.call_soon_threadsafe(event.set)
    loop.call_soon_threadsafe(event.setWithValue("456"))
  
  
# async def handle_client(client):
#     loop = asyncio.get_event_loop()
#     request = None

#     while request != 'quit':
#         request = (await loop.sock_recv(client, 255)).decode('utf8')
#         response = str(request) + '\n'
#         print(response)
#         await loop.sock_sendall(client, response.encode('utf8'))
#     client.close()

# async def run_server():
#     server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     server.bind(('localhost', 8888))
#     server.listen(8)
#     server.setblocking(False)

#     loop = asyncio.get_event_loop()

#     while True:
#         client, _ = await loop.sock_accept(server)
#         loop.create_task(handle_client(client))

# asyncio.run(run_server())

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor
from twisted.internet.protocol import Protocol
from twisted.protocols.basic import LineReceiver

import logging

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@dataclass
class Instruction:
  command: str
  parameters: list[any]

UTF8 = "utf-8"

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

def res_code(b: int):
  return b.to_bytes(1, 'big')

class InstructionProtocol(Protocol):
  def connectionMade(self):
    logger.info(f"Connected to {self.transport.getPeer().host}")

  def dataReceived(self, data):
    logger.debug(f"{self.transport.getPeer().host} sent \"{data}\"")
    
    try:
      instr, = parse_data(data.decode(UTF8))
      print(instr)
    except Exception:
      print("oh no")
    self.transport.write(res_code(0xFA))


class InstructionFactory(Factory):
  def buildProtocol(self, addr):
    return InstructionProtocol()

# 8007 is the port you want to run under. Choose something >1024
endpoint = TCP4ServerEndpoint(reactor, 8888)
endpoint.listen(InstructionFactory())
reactor.run()

# def lineReceived(self, data):
#   logger.debug(f"{self.transport.getPeer().host} sent \"{data}\"")
#   dec = data.decode("utf-8")
#   try:
#     instr = self.parse_instruction(dec)
#     print(instr)
#   except Exception:
#     print("oh no")
#   self.sendLine("ACK".encode("utf-8"))
#   return super().dataReceived(data)

# def parse_instruction(text: str):
#   text = text.strip().rstrip(";")
#   command, parameters = text.split(":", 1)
#   return Instruction(command, parameters.split(";"))

# async def handle_client(reader, writer):
#     request = None
#     while True:
#         request = (await reader.read(255)).decode('utf8')

#         response = "ERROR"
#         # dec = data.decode("utf-8")
#         try:
#           instr = parse_instruction(request)
#           print(instr)
#           response = "ACK: " + str(request) + '\n'
#         except Exception:
#           print("oh no")
#         writer.write(response.encode('utf8'))
#         await writer.drain()
#     writer.close()

# async def run_server():
#   server = await asyncio.start_server(handle_client, 'localhost', 8888)
#   async with server:
#     await server.serve_forever()

# asyncio.run(run_server())

# RunnerThread().start()

# loop.run_until_complete(main())








