import { HsvaColor } from '@uiw/color-convert';
import ShadeSlider from '@uiw/react-color-shade-slider';
import Wheel from '@uiw/react-color-wheel';
import './style.css';

type _HsvColorInputProps = {
  color: HsvaColor
  onChange: (newColor: HsvaColor) => void
}

export type HsvColorInputProps =
  _HsvColorInputProps
  & Omit<React.DetailedHTMLProps<React.HTMLAttributes<HTMLDivElement>, HTMLDivElement>, keyof _HsvColorInputProps>

export default function HsvColorInput({ className, color, onChange }: HsvColorInputProps) {
  return (
    <div className={'rgbSlider' + (className ? ' ' + className : '')}>
      <Wheel color={color} onChange={({ hsva }) => onChange({ ...color, ...hsva })} />
      <ShadeSlider hsva={color} width={316} onChange={({ v }) => onChange({ ...color, v })} />
    </div>
  )
}
