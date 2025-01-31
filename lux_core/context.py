from dataclasses import dataclass

from lux_core.display import Display


@dataclass
class LuxContext:
  display: Display
  target_fps = 60.0
  debug_display: bool = False