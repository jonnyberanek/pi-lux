import React, { useEffect, useState } from 'react';
import logo from './triangle.svg';
import './App.css';
import RgbSlider, {colorSubject} from './RgbSlider'

import { throttleTime, debounceTime } from "rxjs/operators";
import axios from 'axios'
import Color from 'color';

const throttledColorSubject = colorSubject.pipe(
  throttleTime(200, undefined, { leading: true, trailing: true })
); 

throttledColorSubject.subscribe({
  next: async (c) => {
    // console.log(c)
    let res
    try{
      res = await axios.post('http://192.168.0.175:4061/testnet', {
        color: c
      }, {

      })
    } catch(e){
      console.log(e.request, e.response)
    } 
    console.log(res)
  }
})

function makeFilter(color: Color){
  console.log(color.hsl().array())
  console.log(color.saturationl(), color.saturationv(), color.luminosity())
  const brightness = Math.max(...color.rgb().array())/255*75
  console.log({brightness})
  return `sepia(100%) 
    saturate(${380*color.saturationv()/100}%) 
    hue-rotate(${300+color.hue()}deg) 
    brightness(${brightness+75}%)
    `
}

function App() {

  const [color, setColor] = useState<Color>(Color(colorSubject.value))

  useEffect(() => {
    const sub = colorSubject.subscribe({
      next: (color) => {
        setColor(Color(color))
      }
    })
    return sub.unsubscribe
  }, [colorSubject])

  return (
    <div className="App">
      <header className="App-header" style={{
        filter: makeFilter(color)
      }}>
        <img src={logo} className="App-logo" alt="logo" style={{
          marginBottom: 10
          // filter: makeFilter(color)
        }} />
        {/* <div style={{height: 50, width: 50, borderRadius: 4, backgroundColor: color.hex()}}/> */}
        <RgbSlider/>
      </header>
    </div>
  );
}

export default App;
