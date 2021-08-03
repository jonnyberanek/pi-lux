import { RouteComponentProps } from '@reach/router'
import axios from 'axios'
import { FC, useEffect, useMemo, useState } from 'react'
import './scripts.css'

export interface ScriptsScreenProps extends RouteComponentProps {}

const URL =
  process.env.NODE_ENV === 'development'
    ? 'http://localhost:4061'
    : 'http://192.168.0.175:4061'

// Mocked currently
async function getScriptsInDir() {
  return axios.get(URL + '/scripts').then(({ data }) => data)
}

async function runScript(name: string) {
  throw 'stub!'
}

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
