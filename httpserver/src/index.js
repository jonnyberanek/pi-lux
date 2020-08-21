import express from 'express'
import {exec} from 'child_process'
import net from 'net'
import cors from 'cors'
import bodyParser from 'body-parser'

const app = express()
const port = 4061

app.use(cors())
app.use(bodyParser.json())

app.get('/', (req, res) => {
  try{

  } catch(e){

  }
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

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
