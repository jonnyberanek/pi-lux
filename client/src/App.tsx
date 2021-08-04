import Color from 'color'
import { useCallback, useEffect } from 'react'
import { throttleTime } from 'rxjs/operators'
import { setColor } from './api'
import './App.css'
import logo from './assets/triangle.svg'
import { colorSubject } from './RgbSlider'
import BaseRouter from './routing/router'
import TabBar from './routing/TabBar'
import { makeFilter } from './util/color'
import { useObservableValue } from './util/rxjs'

const throttledColorSubject = colorSubject.pipe(
  throttleTime(200, undefined, { leading: true, trailing: true })
)

function App() {
  const colorFn = useCallback(value => Color(value), [])

  const color = useObservableValue(
    colorSubject,
    colorFn,
    Color(colorSubject.value)
  ) as Color

  useEffect(() => {
    const sub = throttledColorSubject.subscribe({
      next: setColor,
    })
    return () => sub.unsubscribe()
  })

  const tabs = [
    {
      label: 'Solid',
      path: 'slider',
    },
    {
      label: 'Scripts',
      path: 'scripts',
    },
  ]

  return (
    <div className="App">
      <header
        className="App-header"
        style={{
          filter: makeFilter(color),
        }}
      >
        <img
          src={logo}
          className="App-logo"
          alt="logo"
          style={{
            marginBottom: 10,
          }}
        />
        <br />
        <TabBar tabs={tabs} />
        <br />
        <BaseRouter />
      </header>
    </div>
  )
}

export default App
