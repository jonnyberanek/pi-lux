import axios from 'axios'
import { tap } from 'rxjs'
import { webSocket } from 'rxjs/webSocket'

const piDev = false

const URL = 'ws://localhost:4061'
// process.env.NODE_ENV === 'development' && !piDev
//   ? 'ws://localhost:4061'
//   : 'ws://192.168.0.175:4061'

export function setColor(ws: WebSocket, color: string) {
  // const socketSubject = webSocket(URL)

  if (ws.readyState == WebSocket.OPEN) {
    ws.send(`fill:${color};;`)
  }

  // socketSubject.next("fill:00ff00;;")
  // return socketSubject.pipe(
  // tap(console.log)
  // )
}