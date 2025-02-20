import { HsvaColor, HsvColor } from "@uiw/color-convert"
import { BehaviorSubject, throttleTime } from "rxjs"

export type RgbColor = [red: number, green: number, blue: number]
export type AppState = { color: HsvaColor }

export const colorSubject = new BehaviorSubject<RgbColor>([0, 0, 0])

export const throttledColorSubject = colorSubject.pipe(
  throttleTime(250, undefined, { leading: true, trailing: true })
)


// todo initialize
const state: { color: RgbColor } = {
  color: [1, 2, 3]
}

export const stateSubject = new BehaviorSubject<AppState>({
  color: { h: 0, s: 0, v: 100, a: 1 }
})

function initState() {

}