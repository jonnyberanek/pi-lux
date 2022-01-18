from animations.dainty_rainbow import randomRainbowFade
from animations.lonestar import lonestar
from animations.rainbow_chaser import rainbowChaser
from ledcontroller.animation import Animator
from led_strip_impl import getAppPixelWriter

def main():
  leds = getAppPixelWriter()
  animator = Animator(leds, frequency=30)
  animator.startAnimation(lonestar)

main()