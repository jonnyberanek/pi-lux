import Color from 'color'

export function makeFilter(color: Color) {
  const brightness = (Math.max(...color.rgb().array()) / 255) * 75
  return `sepia(100%) 
    saturate(${(380 * color.saturationv()) / 100}%) 
    hue-rotate(${300 + color.hue()}deg) 
    brightness(${brightness + 75}%)
    `
}
