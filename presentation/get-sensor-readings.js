const getSensorReadings = (callback) => {
/*    callback(null, 25, 45)*/
    callback(null, (Math.floor(Math.random() * (65 - 55 + 1)) + 55)/10, (Math.floor(Math.random() * (15 - 10 + 1)) + 10)/10)
}

module.exports = getSensorReadings