import axios from 'axios'
import Color from 'color'
import { useCallback, useEffect } from 'react'
import { throttleTime } from 'rxjs/operators'
import './App.css'
import { colorSubject, RgbColor } from './RgbSlider'
import BaseRouter from './routing/router'
import logo from './assets/triangle.svg'
import { makeFilter } from './util/color'
import { useObservableValue } from './util/rxjs'
import TabBar from './routing/TabBar'

const throttledColorSubject = colorSubject.pipe(
  throttleTime(200, undefined, { leading: true, trailing: true })
)

async function sendColorUpdate(c: RgbColor) {
  try {
    await axios.post('http://192.168.0.175:4061/testnet', {
      color: [c[0], c[2], c[1]],
    })
  } catch (e) {
    console.log(e.request, e.response)
  }
}

function App() {
  const colorFn = useCallback(value => Color(value), [])

  const color = useObservableValue(
    colorSubject,
    colorFn,
    Color(colorSubject.value)
  ) as Color

  useEffect(() => {
    const sub = throttledColorSubject.subscribe({
      next: sendColorUpdate,
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
