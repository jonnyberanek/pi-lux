import React, { useReducer, SyntheticEvent, Reducer, Props } from "react";
import { BehaviorSubject } from "rxjs";
import { throttleTime } from "rxjs/operators";
import "./style.css";

type Color = [number, number, number];

export const colorSubject = new BehaviorSubject<Color>([0, 0, 0]);

export const throttledColorSubject = colorSubject.pipe(
  throttleTime(250, undefined, { leading: true, trailing: true })
);

function Slider(props:any) {
  return <input type="range" min={0} max={255} {...props} />;
}

enum Pixel {
  RED,
  GREEN,
  BLUE
}

interface Action {
  color: Pixel;
  value: string;
}

let reducer: Reducer<Color, Action>;

reducer = (state: Color, { color, value }: Action) => {
  const val = parseInt(value, 10);

  const newState: Color = [...state] as Color;

  switch (color) {
    case Pixel.RED:
      newState[0] = val;
      break;
    case Pixel.GREEN:
      newState[1] = val;
      break;
    case Pixel.BLUE:
      newState[2] = val;
      break;
  }

  colorSubject.next(newState);

  return newState;
};

export default function RgbSlider({ className } : {className?: string}) {
  const [color, dispatch] = useReducer<Reducer<Color, Action>>(
    reducer,
    colorSubject.value
  );

  const dispatchChange = (color: Pixel) => ({ target }: SyntheticEvent) => {
    // @ts-ignore
    dispatch({ color, value: target.value });
  };

  return (
    <div className={"rgbSlider" + (className ? " " + className : "")}>
      <Slider
        className="redSlider"
        onChange={dispatchChange(Pixel.RED)}
        value={color[0]}
      />
      <Slider
        className="greenSlider"
        onChange={dispatchChange(Pixel.GREEN)}
        value={color[1]}
      />
      <Slider
        className="blueSlider"
        onChange={dispatchChange(Pixel.BLUE)}
        value={color[2]}
      />
    </div>
  );
}
