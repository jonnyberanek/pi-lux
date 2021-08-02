import { RouteComponentProps } from '@reach/router'
import * as React from 'react'
import RgbSlider from '../RgbSlider'
 
export interface SliderScreenProps extends RouteComponentProps {
  
}
 
const SliderScreen: React.FC<SliderScreenProps> = () => {
  return <div>
    <RgbSlider/>
  </div>
}
 
export default SliderScreen