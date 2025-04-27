import * as React from 'react'
import { WsClient } from 'src/api'
import HsvColorInput, { HsvColorInputProps } from '../HsvColorInput'
import { stateSubject } from '../state'
import { useSubject } from '../util/rxjs'

export interface SliderScreenProps { }

const SliderScreen: React.FC<SliderScreenProps> = () => {
  const [state, setNext] = useSubject(stateSubject)

  const wsClient = React.useRef<WsClient>(new WsClient()).current

  const handleColorChange: HsvColorInputProps['onChange'] = color => {
    console.log(color)
    setNext(curr => ({ ...curr, color }))
    wsClient.setFill(color)
  }

  return (
    <div>
      <HsvColorInput color={state.color} onChange={handleColorChange} />
    </div>
  )
}

export default SliderScreen
