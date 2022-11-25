
const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const db = require('./queries')
const port = 3001
app.get('/temperatures', db.getTemperatures)

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/temperatures', db.getTemperatures)


app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})