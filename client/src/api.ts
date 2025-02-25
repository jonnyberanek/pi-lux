import { HsvaColor, hsvaToHex } from '@uiw/color-convert'
import { debounceTime, filter, map, ReplaySubject, Subject, throttleTime } from 'rxjs'
import { webSocket, WebSocketSubject } from 'rxjs/webSocket'

const piDev = false

const URL = 'ws://localhost:4061'
// process.env.NODE_ENV === 'development' && !piDev
//   ? 'ws://localhost:4061'
//   : 'ws://192.168.0.175:4061'

export class WsClient {

  // Determines what is sent to ws
  private messageSubject: Subject<string> = new Subject()
  private wsSubject: WebSocketSubject<string> | null = null

  private WS_MAX_INTERVAL = 30
  private WS_TIMEOUT = 1500

  setFill(color: HsvaColor) {
    // is a no-op if we don't have a websocket to send to
    if (!this.ensureWebsocket()) {
      console.debug("no op")
      return
    }

    this.messageSubject.next(`fill:${hsvaToHex(color).slice(1)};;`)
  }

  get closed() {
    return this.messageSubject.closed
  }

  private ensureWebsocket() {
    if (this.wsSubject?.closed ?? true) {
      // Return false if no socket shoul be created yet
      if (this.lastSocketCreatedAt > Date.now() - this.WS_TIMEOUT) {
        return false
      }
      [this.wsSubject] = this.initiateNewWebsocket()
    }
    return true
  }

  private lastSocketCreatedAt = 0

  private initiateNewWebsocket() {
    console.log("new ws")
    const wsErrorSubject = new ReplaySubject<CloseEvent>(1) // TODO: For later use

    const ws = webSocket<string>({
      url: URL,
      serializer: String,
      deserializer: String,
      closeObserver: wsErrorSubject
    })
    this.lastSocketCreatedAt = Date.now()

    wsErrorSubject.pipe(
      filter(it => ![1000, 1005].includes(it.code))
    ).subscribe((it => console.warn("ws closed unexpectedly: ", it)))

    // ws listens to subject values values to websocket(s)
    this.messageSubject.pipe(
      throttleTime(this.WS_MAX_INTERVAL)
    ).subscribe(ws)

    ws.subscribe({
      next: console.log,
      error: console.warn,
      complete: () => {
        timeoutSub.unsubscribe()
        ws.unsubscribe()
      }
    })

    // Have ws connection timeout after inactivity
    const timeoutSub = this.messageSubject.pipe(
      debounceTime(this.WS_TIMEOUT)
    ).subscribe(() => {
      ws.unsubscribe()
    })

    return [ws, wsErrorSubject] as const
  }
}


export function startFillTracking() {
  const ws = webSocket({
    url: 'ws://localhost:4061',
    serializer: String,
    deserializer: String,
  })

  const sliderSubject = new Subject<HsvaColor>()

  // Map values to ws
  sliderSubject.pipe(
    throttleTime(15),
    map(it => `fill:${hsvaToHex(it).slice(1)};;`)
  ).subscribe(ws)

  ws.subscribe()

  // Have connection timeout after inactivity
  sliderSubject.pipe(
    debounceTime(1000)
  ).subscribe(() => {
    console.log("closable, closing...")
    sliderSubject.unsubscribe()
  })

  return sliderSubject
}

export function setColor(ws: WebSocket, color: string) {
  if (ws.readyState == WebSocket.OPEN) {
    ws.send(`fill:${color};;`)
  }
}