import express from 'express'
import {exec, spawn} from 'child_process'
import net from 'net'
import cors from 'cors'
import bodyParser from 'body-parser'
import { readdirSync } from 'fs'
import readArgSchema from './read-args'

const app = express()
const port = 4061
const SCRIPTS_PATH = './scripts'

app.use(cors())
app.use(bodyParser.json())

app.get('/', (req, res) => {
  res.send('hello')
})

app.get('/pyecho', (req,res) => {
  exec(`python ${process.cwd()}/scripts/echo.py ${req.query.name ?? ''}`, (error, stdout, stderr) => {
    if(error){
      res.status(500).send({
        message: error.message,
        ...error
      })
      return
    }
    if(stderr){
      res.status(400).send(stderr)
      return
    }
    res.send(stdout)
  })
})

app.post('/flux', (req,res) => {

  console.warn(req.query)
  
  exec(`python3 ${process.cwd()}/scripts/brightness.py ${(req.query.ct + ' ' + req.query.bri) ?? ''}`, (error, stdout, stderr) => {
    if(error){
      console.error('ERROR', error)
      res.status(500).send({
        message: error.message,
        ...error
      })
      return
    }
    if(stderr){
      console.error('PYERROR', error)
      res.status(400).send(stderr)
      return
    }
    res.send(stdout)
  })
    
})

app.post('/testnet', (req, res) => {
  const socket = net.createConnection(4063,'localhost', () => {
    try{
      socket.write(JSON.stringify(req.body))
      res.send()
    } catch(e){
      res.status(500).send(e)
    } finally {
      socket.destroy()
    }
  })
})

app.get('/scripts', (req, res) => {

  const files = readdirSync(SCRIPTS_PATH)
    .filter(name => name.endsWith('.py'))
    .map(name => name)

  const responseData = files.map((name) => {
    return {
      name,
      argSchema: readArgSchema(SCRIPTS_PATH + '/' + name)
    }
  })
  
  res.send(responseData)
})

app.post('/scripts/:scriptName/run', (req, res) => {
  const {scriptName} = req.params
  const args = JSON.stringify(req.body)

  const makeMsg = (msg) => `[pyscript/${scriptName} (${new Date().toISOString()})]: ${msg}`

  let scriptProcess
  try{
    scriptProcess = spawn('python3', ['-u', `${process.cwd()}/scripts/${scriptName}.py`, args])
  } catch(e){
    res.status(500).send(e.message)
    return
  }

  scriptProcess.on('error', err => {
    console.warn(makeMsg('Error starting script: ' + err.stack ?? err.message))
  })
  scriptProcess.stdout.on('data', (data) => {
    console.info(makeMsg(data))
  })
  scriptProcess.stderr.on('data', err => {
    console.warn(makeMsg(err))
  })
  scriptProcess.on('exit', (code) => {
    console.info(makeMsg('Exited with code ' + code))
  })
  
      
  res.sendStatus(204)
})

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
