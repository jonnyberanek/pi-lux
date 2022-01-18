from lux.app.animations.lonestar import lonestar
from lux.app.animations.rainbow_chaser import rainbowChaser
from lux.app.app_writer import getAppPixelWriter
from lux.core.animation import Animator


def main():
  leds = getAppPixelWriter()
  animator = Animator(leds, frequency=30)
  animator.startAnimation(rainbowChaser())

main()
