const express = require('express');
const { Client } = require("pg");

const app = express();
const port = 3001

app.use(express.json())
app.use(function (req, res, next) {
  res.setHeader('Access-Control-Allow-Origin', 'http://localhost:3000');
  res.setHeader('Access-Control-Allow-Methods', 'GET,POST,PUT,DELETE,OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Access-Control-Allow-Headers');
  next();
});


const client = new Client({
  user: 'postgres',
  host: 'localhost',
  database: 'temperaturedb',
  password: 'password',
  port: 5432
});

client.connect();

const getTemperatures = () => {
  return new Promise(function(resolve, reject) {
    client.query('SELECT * FROM temperatures', (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results.rows);
    })
  }) 
}

app.get("/api", (req, res) => {
  getTemperatures()
  .then(response => {
    res.status(200).send(response);
  })
  .catch(error => {
    res.status(500).send(error);
  })
  res.json({ message: "Hello from server!" });
});


app.listen(port, () => {
  console.log(`Listening on port ${port}`)
})