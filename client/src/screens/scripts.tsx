import { hexToHsva } from '@uiw/color-convert'
import { FC, useEffect, useRef, useState } from 'react'
import HsvColorInput from 'src/HsvColorInput'
import { Spinner } from 'src/spinner'
import { Boxed, InstructionMetadata, ListInstructionsResponse, WsClient } from '../network/api'
import './scripts.css'

export interface ScriptsScreenProps { }

function castError(error: any) {
  return (error instanceof Error && error) || Error(String(error))
}

const ScriptsScreen: FC<ScriptsScreenProps> = () => {

  const [content, setContent] = useState<Boxed<ListInstructionsResponse>>()
  const wsClient = useRef<WsClient>(new WsClient()).current

  const [selectedCommand, setSelectedCommand] = useState<InstructionMetadata>()

  useEffect(() => {
    const sub = wsClient.listInstructions()?.subscribe({
      next: (it) => setContent(it),
      // error: (e) => setContent(castError(e).message)
    })
    return () => sub?.unsubscribe()
  }, [])

  return (
    <div className="container">
      <div className='script-list'>
        {
          !content ? <Spinner /> :
            'error' in content ?
              <div style={{ color: 'red' }}>Error: {content.error}</div> :
              (content.data.map(it => (
                <div
                  key={it.id}
                  className='script-list-item'
                  onClick={() => setSelectedCommand(it)}
                >
                  {it.id}: {it.param_types}
                </div>
              )))
        }

      </div>
      {
        selectedCommand && <div>
          {selectedCommand.param_types.map(it =>
            <ParamItem type={it} />
          )}
        </div>
      }
    </div>
  )
}

function ParamList() {

}

function ParamItem({ type }: { type: string }) {
  switch (type) {
    case 'Color':
      return <HsvColorInput color={hexToHsva("#ffffff")} onChange={() => { }} />
    case 'float':
      return <input type='number' step={0.0001} />
    case 'int':
      return <input type='number' step={1} />
  }
}

export default ScriptsScreen
