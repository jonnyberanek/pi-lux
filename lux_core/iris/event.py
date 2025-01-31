import asyncio
from typing import Generic, TypeVar, Union

T = TypeVar("T")

class DataEvent(asyncio.Event, Generic[T]):
  """
  This retains a value with an asynchronous event until it is cleared. This has
  the opportunity to drop events if "overwritten" by a subsequent `set` before
  it can be consumed. This is expected, this should be used in a realtime
  system, prefer `asyncio.Queue` otherwise.
  """
  data: Union[T | None] = None

  def setWithValue(self, value: T):
    self.data = value
    return self.set()

  def clear(self):
    self.data = None
    return super().clear()
  
  async def waitForValue(self) -> T:
    await super().wait()
    return self.data