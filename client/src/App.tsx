import { color, hsvaToHex } from '@uiw/color-convert'
import { useMemo } from 'react'
import { Outlet } from 'react-router'
import 'src/App.css'
import logo from 'src/assets/triangle.svg'
import { routes } from 'src/routing/router'
import TabBar from 'src/routing/TabBar'
import { stateSubject } from 'src/state'
import { makeFilter } from 'src/util/color'
import { useSubject } from 'src/util/rxjs'
import { toCapitalCase } from 'src/util/string'
import { useResolvedRoute } from './routing/utils'

function App() {
  const [state] = useSubject(stateSubject)

  const children = useResolvedRoute(routes).route.children
  const tabs = useMemo(() => {
    return children!!.map(c => ({
      path: c.path!!,
      label: toCapitalCase(c.path ?? "index")
    }))
  }, [children])

  const c = { ...color(state.color).hsva }
  c.s = c.s * c.v / 100
  c.v = c.v / 8 + 10

  return (
    <div
      className="content"
      style={{
        backgroundColor: hsvaToHex(c)
      }}
    >
      <img
        src={logo}
        className="logo"
        alt="logo"
        style={{
          marginBottom: 10,
          filter: makeFilter(color(state.color)),
        }}
      />
      <TabBar className='nav-tabs' tabs={tabs} />
      <Outlet />
    </div>
  )
}

export default App
