import axios from 'axios';
import Color from 'color';
import { useCallback, useEffect } from 'react';
import { throttleTime } from "rxjs/operators";
import './App.css';
import { colorSubject, RgbColor } from './RgbSlider';
import BaseRouter from './router';
import TabBar from './TabBar';
import logo from './triangle.svg';
import { makeFilter } from './util/color';
import { useObservableValue } from './util/rxjs';


const throttledColorSubject = colorSubject.pipe(
  throttleTime(200, undefined, { leading: true, trailing: true })
); 

async function sendColorUpdate(c: RgbColor){
    try{
      await axios.post('http://192.168.0.175:4061/testnet', {
        color: c
      })
    } catch(e){
      console.log(e.request, e.response)
    }
}

function App() {

  const colorFn = useCallback((value) => Color(value), [])
  
  const color = useObservableValue(colorSubject, colorFn, Color(colorSubject.value)) as Color

  useEffect(() => {
    const sub = throttledColorSubject.subscribe({
      next: sendColorUpdate
    })
    return () => sub.unsubscribe()
  })

  return (
    <div className="App">
      <header className="App-header" style={{
        filter: makeFilter(color)
      }}>
        <img src={logo} className="App-logo" alt="logo" style={{
          marginBottom: 10
          // filter: makeFilter(color)
        }} />
        <br/>
        <TabBar tabs={[
          {
            label: 'Solid',
             path: 'slider'
          },
          {
            label: 'Scripts',
            path: 'scripts'
          }
        ]}/>
        <br/>
        <BaseRouter/> 
      </header>
    </div>
  );
}

export default App;
