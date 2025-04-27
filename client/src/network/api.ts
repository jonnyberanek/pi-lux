import { HsvaColor, hsvaToHex } from '@uiw/color-convert'
import { catchError, map, Observable, of, tap } from 'rxjs'
import { WebsocketConnectionManager, WebSocketError, WebSocketResponse } from './websocket-connectivity'
import { z, ZodError } from 'zod'

const piDev = false

const URL = 'ws://localhost:4061'
// process.env.NODE_ENV === 'development' && !piDev
//   ? 'ws://localhost:4061'
//   : 'ws://192.168.0.175:4061'

// export interface InstructionMetadata {
//   id: string,
//   param_types: string[]
// }

const sGoodResponse = z.object({
  code: z.number(),
  data: z.any()
})

const sBadResponse = z.object({
  code: z.number(),
  error: z.object({
    message: z.string(),
    data: z.string().optional()
  })
})

const sInstructionMetadata = z.object({
  id: z.string(),
  param_types: z.array(z.string())
})
export type InstructionMetadata = z.infer<typeof sInstructionMetadata>

const sListInstructionsResponse = sGoodResponse.extend({
  data: z.array(sInstructionMetadata)
})
export type ListInstructionsResponse = z.infer<typeof sListInstructionsResponse>

const sResponse = z.union([sGoodResponse, sBadResponse])

type WsJsonSuccessResponse = z.infer<typeof sGoodResponse>


// interface WsJsonSuccessResponse<T> extends WebSocketResponse {
//   data: T
// }

// interface WsJsonErrorResponse extends WebSocketResponse {
//   error: {
//     message: string
//     data?: any
//   }
// }

type WsJsonResponse = z.infer<typeof sResponse>

// export type WsJsonResponse<T = any> = WsJsonSuccessResponse<T> | WsJsonErrorResponse

// export type WsResponse<T = any> = number | WsJsonResponse<T>

// Not my favorite, but for now lets assume the consumer of this API is always
//  a view, so it does not need heavy error details
export type Boxed<T extends WsJsonSuccessResponse> =
  | { data: T['data'] }
  | { error: string }

function castError(error: any) {
  return (error instanceof Error && error) || Error(String(error))
}

export class WsClient {
  private pfpConnectionManager = new WebsocketConnectionManager(
    deserializePfpMessage,
    { url: URL, protocol: 'pfp' }
  )
  private dfpConnectionManager = new WebsocketConnectionManager(
    deserializeDfpMessage,
    { url: URL, protocol: 'dfp' }
  )

  listInstructions(): Observable<Boxed<ListInstructionsResponse>> {
    return this.dfpConnectionManager.send(sub => {
      sub.next(`!list_instructions;;`)
    }).pipe(
      map(it => {
        if ('error' in it) {
          throw Error(it.error.message)
        }
        return { data: sListInstructionsResponse.parse(it).data }
      }),
      catchError(e => {
        console.warn(e)
        return of({ error: castError(e).message })
      })
    )
    // return defer(() => {
    //   const socket = this.connectionManager.acquireWebsocket()
    //   if (!) {
    //     throw Error("Could not create connection to websocket")
    //   }

    //   this.messageSubject.next(`!list_instructions;;`)

    //   return merge(
    //     this.wsSubject!!,
    //     this.wsErrorSubject!!.pipe(
    //       filter(it => ![1000, 1005].includes(it.code)),
    //       map(it => { throw Error(`Websocket closed unexpectedly: ${it.code}`) })
    //     )
    //   )
    // })
  }

  setFill(color: HsvaColor) {
    return this.pfpConnectionManager.send(sub => {
      sub.next(`fill:${hsvaToHex(color).slice(1)};;`)
    }).subscribe()
  }

  // get closed() {
  //   return this.messageSubject.closed
  // }

  // private ensureWebsocket() {
  //   if (this.wsSubject?.closed ?? true) {
  //     // Return false if no socket shoul be created yet
  //     if (this.lastSocketCreatedAt > Date.now() - this.WS_TIMEOUT) {
  //       return false
  //     }
  //     [this.wsSubject, this.wsErrorSubject] = this.initiateNewWebsocket()
  //   }
  //   return true
  // }

  // private lastSocketCreatedAt = 0

  // private initiateNewWebsocket() {
  //   console.log("new ws")
  //   const wsErrorSubject = new ReplaySubject<CloseEvent>(1) // TODO: For later use

  //   const ws = webSocket({
  //     url: URL,
  //     serializer: String,
  //     deserializer: deserializeWsMessage,
  //     binaryType: "arraybuffer",
  //     closeObserver: wsErrorSubject
  //   })
  //   this.lastSocketCreatedAt = Date.now()

  //   wsErrorSubject.pipe(
  //     filter(it => ![1000, 1005].includes(it.code))
  //   ).subscribe((it => console.warn("ws closed unexpectedly: ", it)))

  //   // ws listens to subject values and sends to websocket
  //   this.messageSubject.pipe(
  //     throttleTime(this.WS_MAX_INTERVAL)
  //   ).subscribe(ws)

  //   ws.subscribe({
  //     next: console.log,
  //     error: console.warn,
  //     complete: () => {
  //       timeoutSub.unsubscribe()
  //       ws.unsubscribe()
  //     }
  //   })

  //   // Have ws connection timeout after inactivity
  //   const timeoutSub = this.messageSubject.pipe(
  //     debounceTime(this.WS_TIMEOUT)
  //   ).subscribe(() => {
  //     ws.unsubscribe()
  //   })

  //   return [ws, wsErrorSubject] as const
  // }
}

function deserializeDfpMessage(data: any): WsJsonResponse {
  try {
    return sResponse.parse(JSON.parse(data))
  } catch (e) {
    console.log(e)
    const message = e instanceof SyntaxError ? "Not valid JSON"
      : e instanceof ZodError ? "Invalid format"
        : "An Unknown parsing error occurred"
    throw new WebSocketError(`Unsupported return type: Could not parse response - ${message}`)
  }
}

function deserializePfpMessage(data: any): WebSocketResponse {
  console.log(data,)
  if (!(data instanceof ArrayBuffer)) {
    throw new WebSocketError(`Unsupported return type: Expected binary but received '${typeof data}'`)
  }
  return { code: new DataView(data).getUint8(0) }
}


