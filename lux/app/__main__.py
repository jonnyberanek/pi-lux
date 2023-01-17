import time

from lux.app.coordinator import SimpleCoordinator
from lux.app.display.displays.cli_display import CliIndexDisplay
from lux.app.instructions.chaser_instruction import ChaserInstruction
from lux.core2.timely import TimeInstant

if __name__ == "__main__":
  print("running test")
  coordinator = SimpleCoordinator(CliIndexDisplay(15))
  coordinator.instruction = ChaserInstruction()

  # This is the "Animator"
  for i in range(10):
    coordinator.updateDisplays(TimeInstant(time.time()))
    time.sleep(0.01)