const {readFileSync} = require('fs')

function readArgSchema(filename) {
  const data = readFileSync(filename).toString()

  const args = data.match(/""" *JSON-ARGS\s*{[\s\S]+?}\s*"""/g)
  
  if(!args || args.length === 0) return null
  else {
    const schema = args[0]
      // Remove top boundary
      .replace(/""" *JSON-ARGS\s*/, '')
      // Remove bottom boundary
      .replace(/\s*"""\s*$/, '')
    return JSON.parse(schema)
  }
}

module.exports = readArgSchema