import { useCallback, useEffect, useState } from 'react'
import { BehaviorSubject, Observable, Subject } from 'rxjs'

export function useObservableValue<O, V = O>(
  subject: Subject<O>,
  getValueFn?: (value: O) => V,
  initialValue?: V
) {
  const [value, setValue] = useState(initialValue)

  useEffect(() => {
    const subscription = subject.subscribe({
      next: value => {
        //@ts-ignore
        setValue(getValueFn?.(value) ?? value)
      },
    })
    return () => subscription.unsubscribe()
  }, [subject, getValueFn])

  return value
}

export function useSubject<V>(
  subject: BehaviorSubject<V>,
) {
  const [value, setValue] = useState(subject.value)

  useEffect(() => {
    const sub = subject.subscribe({
      next: value => {
        setValue(value)
      },
    })
    return () => sub.unsubscribe()
  }, [subject])

  // const setNext = useCallback(, [subject, subject.value])

  const setNext = (fn: (current: V) => V) => {
    subject.next(fn(subject.value))
  }

  return [value, setNext] as const
}

