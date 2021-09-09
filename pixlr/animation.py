from typing import Callable, Generator
from pixlr.strip import PixelStripWriter
from time import sleep

class Animator():
  """
  This class composes a writer and animations to handle an animation.

  This standardizes the animation producer and guarantees the animation never
  depends on a specific implementation of PixelStripWriter.
  """

  writer: PixelStripWriter

  def __init__(self, writer=None, frequency=60) -> None:
    self.writer = writer
    self.frequency = frequency

  def startAnimation(self, animation: Callable[[PixelStripWriter], Generator]):
    for _ in animation(self.writer):
      # Sleep between frames for frequency
      sleep(1/self.frequency)
