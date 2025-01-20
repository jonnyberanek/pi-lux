from time import perf_counter

from sdl2 import SDL_Delay as sleep

class FramerateRectifier():
  target_fps: float = 30.0
  last_sleep_time: float = perf_counter()

  def tick(self) -> float:
    sleep(int(max(0, 1/self.target_fps - (perf_counter() - self.last_sleep_time)) * 1000))
    self.last_sleep_time = perf_counter()