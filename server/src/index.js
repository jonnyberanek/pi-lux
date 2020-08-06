import express from 'express'
import {exec} from 'child_process'

const app = express()
const port = 3000

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
  
  exec(`python3 ${process.cwd()}/scripts/luxed.py ${(req.query.ct + ' ' + req.query.bri) ?? ''}`, (error, stdout, stderr) => {
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

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
