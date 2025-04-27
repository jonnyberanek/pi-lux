from ctypes import c_ubyte
from typing import Callable
from lux_core.beam.core import BeamException, BeamRequest, res_code
from lux_core.beam.protocols.handler import ProtocolHandler

type Result = c_ubyte | None
type OnPfpRequestParsedHandler = Callable[[list[BeamRequest]], Result]

class PfpProtocolHandler(ProtocolHandler):

  def __init__(self, handle: OnPfpRequestParsedHandler) -> None:
    super().__init__()
    self.handle = handle

  def handle_requests(self, requests: list[BeamRequest]) -> bytes:  
    res = self.handle(requests[-1:])
    return res_code(0x0 if res is None else res)

  def handle_exception(self, exception: Exception) -> bytes:
    if isinstance(exception, BeamException):
      return res_code(exception.code)
    return res_code(0xFF) # Unknown error