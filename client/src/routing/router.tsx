import { Router } from '@reach/router'
import ScriptsScreen from '../screens/scripts'
import SliderScreen from '../screens/slider'

const BaseRouter = ({}) => {
  return (
    <Router>
      <SliderScreen path="slider" />
      <ScriptsScreen path="scripts" />
    </Router>
  )
}

export default BaseRouter
