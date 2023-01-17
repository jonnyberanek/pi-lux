from abc import abstractmethod
from dataclasses import dataclass

from lux.core2.timely import TimeInstant

@dataclass
class IntervalTimeData(TimeInstant):
  interval: float

  @property
  def intervalTime(self):
    return self.time % self.interval

  @property
  def intervalPercent(self):
    return self.intervalTime / self.interval

class Intervaled():

  @property
  @abstractmethod
  def interval(self) -> float:
    pass
  
  def getIntervalTimeInstant(self, instant: TimeInstant):
    return IntervalTimeData(instant.time, self.interval)
