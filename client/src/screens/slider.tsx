import * as React from 'react'
import HsvColorInput, { HsvColorInputProps } from '../HsvColorInput'
import { useSubject } from '../util/rxjs'
import { stateSubject } from '../state'
import { matchRoutes, useLocation, useMatch, useMatches, useResolvedPath } from 'react-router'
import { routes } from 'src/routing/router'
import { useResolvedRoute } from 'src/routing/utils'

export interface SliderScreenProps { }

const SliderScreen: React.FC<SliderScreenProps> = () => {
  const [state, setNext] = useSubject(stateSubject)

  const handleColorChange: HsvColorInputProps['onChange'] = color => {
    setNext(curr => ({ ...curr, color }))
  }

  return (
    <div>
      <HsvColorInput color={state.color} onChange={handleColorChange} />
    </div>
  )
}

export default SliderScreen
