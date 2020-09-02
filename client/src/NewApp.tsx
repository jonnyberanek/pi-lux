import React from 'react';
import logo from './logo.svg';
import './App.css';
import RgbSlider, {colorSubject} from './RgbSlider'

import { throttleTime, debounceTime } from "rxjs/operators";
import axios from 'axios'

const throttledColorSubject = colorSubject.pipe(
  throttleTime(200, undefined, { leading: true, trailing: true })
); 

throttledColorSubject.subscribe({
  next: async (c) => {
    console.log(c)
    let res
    try{
      res = await axios.post('http://192.168.1.223:4061/testnet', {
        color: c
      }, {

      })
    } catch(e){
      console.log(e.request, e.response)
    } 
    console.log(res)
  }
})

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <RgbSlider/>
      </header>
    </div>
  );
}

export default App;
