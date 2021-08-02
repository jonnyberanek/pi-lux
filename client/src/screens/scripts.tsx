import { RouteComponentProps } from '@reach/router'
import * as React from 'react'

export interface ScriptsScreenProps extends RouteComponentProps {}

const ScriptsScreen: React.FC<ScriptsScreenProps> = () => {
  return (
    <div>
      <div style={{ color: 'white' }}>scripts</div>
    </div>
  )
}

export default ScriptsScreen
