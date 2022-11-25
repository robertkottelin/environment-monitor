const express = require('express')
const bodyParser = require('body-parser')
const { response } = require('express')
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

pool.connect()
// pool.query('SELECT * FROM temperatures;', (error, results) => {
//     if (error) {
//         throw error;
//     } else {
//       response.status(200).json(results.rows)
//     }
// });


const getTemperatures = (request, response) => {
  pool.query('SELECT * FROM temperatures;', (error, results) => {
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
console.log()


app.listen(port, () => {
  console.log(`App running on port ${port}.`)
})