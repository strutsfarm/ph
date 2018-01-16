const getSensorReadings = require('./get-sensor-readings')

/**
 * Import the database module that we created earlier
 */
const databaseOperations = require('./database-operations')

const cache = {
  temperature: 0,
  humidity: 0
}

setInterval(() => {
    databaseOperations.fetchReading('temp', (err, results) => {
    if (err) {
      console.error(err)
    }
    cache.temperature = results.measured_pH
    cache.humidity = results.measured_Ec
  })
}, 2000)

module.exports.getTemperature = () => cache.temperature
module.exports.getHumidity = () => cache.humidity
