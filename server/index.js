import express from 'express'

const app = express()
const port = 3000

app.get('/', (req, res) => {
  try{

  } catch(e){

  }
  res.send('hello')
})

app.listen(port, () => console.log(`Example app listening at http://localhost:${port}`))
