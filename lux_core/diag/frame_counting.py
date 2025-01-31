from threading import Event, Thread
from time import sleep, perf_counter as time

class StoppableThread(Thread):
  """Thread class with a stop() method. The thread itself has to check
  regularly for the stopped() condition."""

  def __init__(self,  *args, **kwargs):
    super(StoppableThread, self).__init__(*args, **kwargs)
    self._stop_event = Event()

  def stop(self):
    self._stop_event.set()

  @property
  def stopped(self):
    return self._stop_event.is_set()

class FrameCounterThread(StoppableThread):
  total_count = 0.0
  count = 0.0

  def __init__(self, tag = "MAIN", do_total = False, *args, **kwargs):
    super(self.__class__, self).__init__(*args, **kwargs)
    self.tag = tag
    self.do_total = do_total
    self.daemon = True

  def run(self):
    start_time = time()
    last_check = time()
    while not self.stopped:
      sleep(1.0)
      now = time()
      count = self.count
      print(f"[{self.tag}] Average frames is {count / (now - last_check)}{f' (Total {self.total_count / (now - start_time)})' if self.do_total else ''}")
      self.count = 0.0
      last_check = time()
  
  def inc_count(self):
    self.count += 1
    self.total_count += 1