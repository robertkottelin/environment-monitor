
const express = require('express')
const bodyParser = require('body-parser')
const app = express()
const port = 3001

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

const Pool = require('pg').Pool
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'temperaturedb',
    password: 'password',
    port: 5432
  });



const getTemperatures = (request, response) => {
    pool.connect()
    pool.query('SELECT * FROM temperatures', (error, results) => {
        if (error) {
            throw error;
        }
        response.status(200).json(results.rows);
        console.log('success')
    });
};


app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/temperatures', db.getTemperatures)


app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})