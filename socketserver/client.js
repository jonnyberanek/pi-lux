const net = require('net')

const client = net.createConnection(9999, 'localhost', () => {
  console.log('connected!')
  client.write(JSON.stringify({
    action: 'fill',
    color: [0,0,1]
  }))
})
