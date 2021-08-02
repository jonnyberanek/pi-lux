import { useEffect, useState } from 'react'
import { Subject } from 'rxjs'

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
