import { debounceTime, defer, filter, ignoreElements, map, merge, MonoTypeOperatorFunction, Observable, OperatorFunction, pipe, ReplaySubject, Subject, throttleTime } from 'rxjs'
import { webSocket, WebSocketSubject, WebSocketSubjectConfig } from 'rxjs/webSocket'

export class WebSocketError extends Error { }
export class WebSocketUnavailableError extends WebSocketError { }
export class WebSocketClosedError extends WebSocketError {

  constructor(
    readonly code: number,
    message?: string
  ) {
    super(`Websocket closed unexpectedly [${code}]${message ? `: ${message}` : ''}`)
  }
}
export class WebSocketResponseError extends WebSocketError {
  constructor(
    readonly code: number,
    message?: string
  ) {
    super(`Websocket responded in error [${code}]${message ? `: ${message}` : ''}`)
  }
}

type WebSocketConnectionConfig = {
  url: string
  maxInterval: number
  timeout: number
  protocol: string
}

export interface WebSocketResponse {
  code: number,
  [k: string]: any
}

type Deserializer<T extends WebSocketResponse> = (data: any) => T
type WebsocketErrorSubject = ReplaySubject<CloseEvent>

type WebSocketFactory = (...args: ConstructorParameters<Required<WebSocketSubjectConfig<any>>['WebSocketCtor']>) => WebSocket

export class WebsocketConnectionManager<T extends WebSocketResponse> {

  // Determines what is sent to ws
  private messageSubject: Subject<string> = new Subject()

  private wsSubjects: {
    ws: WebSocketSubject<any>,
    error: WebsocketErrorSubject
  } | null = null

  get currentSocket() {
    return this.wsSubjects?.ws
  }

  private config: WebSocketConnectionConfig

  private defaultConfig: Omit<WebSocketConnectionConfig, 'url' | 'protocol'> = {
    maxInterval: 30,
    timeout: 1500
  }

  constructor(
    readonly deserializer: Deserializer<T>,
    // readonly webSocketFactory: WebSocketFactory = (...args) => new WebSocket(...args),
    config: Pick<WebSocketConnectionConfig, 'url' | 'protocol'> & Partial<WebSocketConnectionConfig>
  ) {
    this.config = { ...this.defaultConfig, ...config }
  }

  send(fn: (req: Subject<string>) => void): Observable<T> {
    return defer(() => {
      const subjects = this.acquireWebsocket()
      fn(this.messageSubject)

      // TODO: consider ws.pipe(takeUntil(errSub), ...) <-- this makes more sense (only) for DFP requests
      // See: https://stackoverflow.com/questions/65188540/rxjs-error-observable-when-another-emits-value
      return mergeWebsocketStreams<T>(subjects.ws.pipe(map(this.deserializer)), subjects.error) // TODO
    })
  }

  acquireWebsocket(): NonNullable<typeof this.wsSubjects> {
    let subjects = this.wsSubjects
    if (!subjects || subjects.ws.closed || subjects.error.closed) {
      // Return false if no socket should be created yet
      if (this.lastSocketCreatedAt > Date.now() - this.config.timeout) {
        throw new WebSocketUnavailableError("Rate limited - too many new connection requests")
      }
      subjects = this.initiateNewWebsocket()
      this.wsSubjects = subjects
    }
    return subjects
  }

  private lastSocketCreatedAt = 0

  private initiateNewWebsocket(): NonNullable<typeof this.wsSubjects> {
    console.log("new ws")
    const wsErrorSubject = new ReplaySubject<CloseEvent>(1) // TODO: For later use

    let ws = webSocket<any>({
      url: this.config.url,
      serializer: String,
      deserializer: (event) => event.data,
      binaryType: "arraybuffer",
      closeObserver: wsErrorSubject,
      protocol: this.config.protocol
      // WebSocketCtor: this.webSocketFactory TODO
    })
    this.lastSocketCreatedAt = Date.now()

    wsErrorSubject.pipe(
      filter(it => ![1000, 1005].includes(it.code))
    ).subscribe((it => console.warn("ws closed unexpectedly: ", it)))

    // ws listens to subject values and sends to websocket
    this.messageSubject.pipe(
      throttleTime(this.config.maxInterval)
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
      debounceTime(this.config.timeout)
    ).subscribe(() => {
      ws.unsubscribe()
    })

    return { ws, error: wsErrorSubject }
  }
}


export const handleWebsocketClose: OperatorFunction<CloseEvent, never> =
  pipe(
    filter(it => ![1000, 1005].includes(it.code)),
    map(it => { throw new WebSocketClosedError(it.code) }),
    ignoreElements()
  )


export function mapWebsocketResponse<T extends WebSocketResponse>(): MonoTypeOperatorFunction<T> {
  return map(it => {
    if (it.code >= 0x1) {
      throw new WebSocketResponseError(it.code)
    }
    return it
  })
}

export function mergeWebsocketStreams<T extends WebSocketResponse>(response$: Observable<T>, error$: WebsocketErrorSubject): Observable<T> {
  return merge(
    response$.pipe(mapWebsocketResponse()),
    error$.pipe(handleWebsocketClose)
  )
}

// function deserializeWsMessage(message: MessageEvent): WebSocketResponse {
//   const data = message.data
//   if (data instanceof ArrayBuffer) {
//     return { code: new DataView(data).getUint8(0) }
//   }
//   // TODO
//   return {
//     code: 0,
//     // data: JSON.parse(data)
//   };
// }

// const wcm = new WebsocketConnectionManager(deserializeWsMessage, { url: "" })

// wcm.send((msg$) => {
//   msg$.next("clear;;")
// }).pipe(
//   asdasd
// ).subscribe