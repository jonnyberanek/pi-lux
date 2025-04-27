import { describe, expect, test, beforeEach, suite, vi } from 'vitest'
import { mapWebsocketResponse, mergeWebsocketStreams, WebSocketClosedError, WebsocketConnectionManager, WebSocketResponse, WebSocketResponseError } from './websocket-connectivity'
import { TestScheduler } from 'rxjs/testing'

describe(mergeWebsocketStreams.name, () => {

  const SUCCESS = 0x0
  const ERROR = 0X10

  let testScheduler
  beforeEach(() => {
    testScheduler = new TestScheduler((actual, expected) => {
      expect(actual).deep.equal(expected)
    })
  })

  test('emits value on success code', () => {

    testScheduler.run(({ cold, expectObservable }) => {
      const marbles = '-a';
      const values = { a: { code: SUCCESS } }

      expectObservable(
        mergeWebsocketStreams(
          cold(marbles, values),
          cold('')
        )
      ).toBe(marbles, values)
    })
  })

  test('handles multiple emits', () => {

    testScheduler.run(({ cold, expectObservable }) => {
      const marbles = '-a-a-b';
      const values = { a: { code: SUCCESS }, b: { code: ERROR } }

      expectObservable(
        mergeWebsocketStreams(
          cold(marbles, values),
          cold('')
        )
      ).toBe('-a-a-#', values, new WebSocketResponseError(ERROR))
    })

  })

  test('emits response error on error code', () => {

    testScheduler.run(({ cold, expectObservable }) => {

      expectObservable(
        mergeWebsocketStreams(
          cold('-a', { a: { code: ERROR } }),
          cold('')
        )
      ).toBe('-#', {}, new WebSocketResponseError(ERROR))
    })
  })

  const testCloseSuccess = (code) => test('ignores close with code ' + code, () => {

    testScheduler.run(({ cold, expectObservable }) => {

      expectObservable(
        mergeWebsocketStreams(
          cold('---'),
          cold('-c', { c: { code } })
        )
      ).toBe('---')
    })
  })

  testCloseSuccess(1000)
  testCloseSuccess(1005)

  test('emits error on close with bad code', () => {
    const CLOSE_CODE = 1002
    testScheduler.run(({ cold, expectObservable }) => {

      expectObservable(
        mergeWebsocketStreams(
          cold('---'),
          cold('-c', { c: { code: CLOSE_CODE } })
        )
      ).toBe('-#', undefined, new WebSocketClosedError(CLOSE_CODE))
    })
  })
})

// suite(WebsocketConnectionManager.name, () => {
//   let wcm
//   beforeEach(() => {
//     wcm = new WebsocketConnectionManager(
//       () => { },
//       () => new WebSocket(),
//       { url: "" }
//     )
//   })

//   test("", () => {
//     vi.fn()
//   })
// })