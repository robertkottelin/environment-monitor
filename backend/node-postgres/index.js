const express = require('express');
const { Client } = require("pg");
const bodyParser = require('body-parser');

const app = express();
const port = 3001

app.use(express.json())
app.use(function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers');
  next();
});

app.use(bodyParser.json());
app.use(
  bodyParser.urlencoded({
    extended: true,
  })
);

const client = new Client({
  user: 'postgres',
  host: 'localhost',
  database: 'temperaturedb',
  password: 'password',
  port: 5432
});

client.connect();

const getTemperatures = (request, response) => {
  client.query('SELECT * FROM temperatures', (error, results) => {
    if (error) {
      throw error;
    }
    response.status(200).json(results.rows);
  });
};

app.get('/', (request, response) => {
  response.json({ info: 'Node.js, Express, and Postgres API' });
});

app.get('/temperatures', getTemperatures);

app.listen(port, () => {
  console.log(`Listening on port ${port}`)
})
