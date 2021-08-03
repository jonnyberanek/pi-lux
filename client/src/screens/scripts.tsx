import { RouteComponentProps } from '@reach/router'
import axios from 'axios'
import { FC, useEffect, useState } from 'react'
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
  const [scripts, setScripts] = useState<string[] | string>()

  console.log(scripts)

  useEffect(() => {
    getScriptsInDir()
      .then(list => {
        setScripts(list)
      })
      .catch(e => {
        console.warn(e.stack)
        setScripts(e.message)
      })
  }, [])

  return (
    <div className="container">
      {!scripts ? (
        <div>Loading...</div>
      ) : typeof scripts === 'string' ? (
        <div style={{ color: 'red' }}>Error: {scripts}</div>
      ) : (
        <div className='script-list'>
          {scripts.map(x => (
            <div
              className='script-list-item'
              onClick={() => runScript(x)}
            >
              {x}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default ScriptsScreen
