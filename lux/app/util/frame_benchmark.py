from collections import deque
from time import time

class FrameBenchmark():

  frameTimes = deque()

  def __init__(self, maxHistory = 100) -> None:
    self.maxHistory = maxHistory
  
  def add(self):
    self.frameTimes.append(time())
    if(len(self.frameTimes) > self.maxHistory):
      self.frameTimes.popleft()

  def logTime(self):
    length = len(self.frameTimes)
    if(length >= self.maxHistory):
      print(f"Average frame time is {length / (self.frameTimes[length-1] - self.frameTimes[0]) }")
    else:
      print("Gathering frame data..")