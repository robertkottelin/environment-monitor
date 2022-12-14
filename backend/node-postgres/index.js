const express = require('express')
const bodyParser = require('body-parser')
const { response } = require('express')
const app = express()
const port = 3001
const hostname = '192.168.0.15';

app.use(bodyParser.json())
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
)

const Pool = require('pg').Pool

// Only for testing, replace with .env file
const pool = new Pool({
    user: 'postgres',
    host: '192.168.0.39',
    database: 'temperaturedb',
    password: 'password',
    port: 5432
  });

pool.connect()

const getTemperatures = (request, response) => {
  pool.query('SELECT * FROM temperatures ORDER BY temperatures.id DESC LIMIT 1000;', (error, results) => {
      if (error) {
          throw error;
      }
      response.status(200).json(results.rows);
  });
};

const getChartData = (request, response) => {
  pool.query('SELECT * FROM temperatures ORDER BY temperatures.id DESC LIMIT 100;', (error, results) => {
      if (error) {
          throw error;
      }
      response.status(200).json(results.rows);
  });
};
const getCurrentTemperature = (request, response) => {
  pool.query('SELECT * FROM temperatures ORDER BY temperatures.id DESC LIMIT 1;', (error, results) => {
      if (error) {
          throw error;
      }
      response.status(200).json(results.rows);
  });
};

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' })
})

app.get('/temperatures', getTemperatures)
app.get('/chartdata', getChartData)
app.get('/currenttemperature', getCurrentTemperature)
// console.log()


app.listen(port, hostname, () => {
  console.log(`App running on port http://${hostname}:${port}`)
})