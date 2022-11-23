const Pool = require('pg').Pool

const pool = new Pool({
  user: 'postgres',
  host: 'localhost',
  database: 'temperatures',
  password: 'password',
  port: 5432,
});

const getTemperatures = () => {
  return new Promise(function(resolve, reject) {
    pool.query('SELECT * FROM temperatures', (error, results) => {
      if (error) {
        reject(error)
      }
      resolve(results.rows);
    })
  }) 
}


module.exports = {
  getTemperatures,
}