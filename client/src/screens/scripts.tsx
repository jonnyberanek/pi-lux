import { RouteComponentProps } from '@reach/router'
import { FC, useEffect, useState } from 'react'
import { getScriptsInDir, runScript } from '../api'
import './scripts.css'

export interface ScriptsScreenProps extends RouteComponentProps {}

const ScriptsScreen: FC<ScriptsScreenProps> = () => {
  const [scriptData, setScriptData] = useState<{name: string, argSchema: any}[] | string>()

  useEffect(() => {
    getScriptsInDir()
      .then(list => {
        setScriptData(list)
      })
      .catch(e => {
        console.warn(e.stack)
        setScriptData(e.message)
      })
  }, [])

  return (
    <div className="container">
      {!scriptData ? (
        <div>Loading...</div>
      ) : typeof scriptData === 'string' ? (
        <div style={{ color: 'red' }}>Error: {scriptData}</div>
      ) : (
        <div className='script-list'>
          {scriptData.map(x => (
            <div
              className='script-list-item'
              onClick={() => runScript(x.name)}
            >
              {x.name.slice(0,x.name.length-3)}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ScriptsScreen
