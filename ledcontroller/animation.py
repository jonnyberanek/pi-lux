from typing import Callable, Generator
from ledcontroller.strip import PixelDisplayWriter
from time import sleep

class Animator():
  """
  This class composes a writer and animations to handle an animation.

  This standardizes the animation producer and guarantees the animation never
  depends on a specific implementation of PixelStripWriter.
  """

  writer: PixelDisplayWriter

  def __init__(self, writer=None, frequency=60) -> None:
    self.writer = writer
    self.frequency = frequency

  def startAnimation(self, animation: Callable[[PixelDisplayWriter], Generator]):
    for _ in animation(self.writer):
      # Sleep between frames for frequency
      sleep(1/self.frequency)
