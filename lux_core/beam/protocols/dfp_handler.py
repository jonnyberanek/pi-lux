from abc import ABC
from dataclasses import dataclass, is_dataclass
import json
from typing import Any, Callable
from lux_core.beam.core import BeamException, BeamRequest, res_code
from lux_core.beam.protocols.handler import ProtocolHandler

type Result = Any
type OnDfpRequestParsedHandler = Callable[[BeamRequest], Result]

EMPTY = object()

def error_response(code: int, message: str, data: Any = EMPTY):
  d = {
    'code': code,
    'error': {
      'message': message
    }
  }
  if data is not EMPTY:
    d['error']['data'] = data
  return d

def success_response(code: int, data: Any = EMPTY):
  d = {
    'code': code
  }
  if data is not EMPTY:
    d['data'] = data
  return d

class DfpProtocolHandler(ProtocolHandler):

  def __init__(self, handle: OnDfpRequestParsedHandler) -> None:
    super().__init__()
    self.handle = handle

  def handle_requests(self, requests: list[BeamRequest]) -> str:  
    data = self.handle(requests[-1])
    return json.dumps(success_response(0, EMPTY if data is None else data), default=vars)

  def handle_exception(self, exception: Exception) -> str:
    if isinstance(exception, BeamException):
      return json.dumps(error_response(int(exception.code), "TODO"))
    return json.dumps(error_response(0xFF, "TODO")) # Unknown error