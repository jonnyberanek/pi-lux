import React from 'react';
import logo from './logo.svg';
import './App.css';
import RgbSlider from './RgbSlider'

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
