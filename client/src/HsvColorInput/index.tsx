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
      <Wheel className='wheel' style={{ width: 316, height: 316 }} color={color} onChange={({ hsva }) => onChange({ ...color, ...hsva })} />

      <div className='slider-row'>
        <button onClick={() => onChange({ ...color, v: 0 })}>Off</button>
        <ShadeSlider className='slider' hsva={color} onChange={({ v }) => onChange({ ...color, v })} />
      </div>
    </div>
  )
}
