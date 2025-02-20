import { ColorResult } from '@uiw/color-convert'

export function makeFilter({ hsv: { h, s, v } }: ColorResult) {
  return `sepia(100%)
    saturate(${s * v / 33}%)
    hue-rotate(${300 + h}deg)
    brightness(${1 * v / 2 + 50}%)
    `
}
