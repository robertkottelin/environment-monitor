const Pool = require('pg').Pool
const pool = new Pool({
    user: 'postgres',
    host: 'localhost',
    database: 'temperaturedb',
    password: 'password',
    port: 5432
  });

const getTemperatures = (request, response) => {
    pool.query('SELECT * FROM temperatures', (error, results) => {
        if (error) {
            throw error;
        }
        response.status(200).json(results.rows);
        console.log('success')
    });
};

module.exports = {
    getTemperatures,
}


