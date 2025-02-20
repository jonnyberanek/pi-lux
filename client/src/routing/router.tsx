import { createBrowserRouter } from 'react-router'
import App from 'src/App'
import ScriptsScreen from 'src/screens/scripts.tsx'
import SliderScreen from 'src/screens/slider.tsx'

export const routes = [
  {
    path: "/",
    element: <App />,
    children: [
      { index: true, path: 'slider', element: <SliderScreen /> },
      { path: 'scripts', element: <ScriptsScreen /> }
    ]
  }
]

const browserRouter = createBrowserRouter(routes)

export default browserRouter
