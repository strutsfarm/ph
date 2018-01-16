const sqlite3 = require('sqlite3').verbose();
const path = require('path')
console.log(path.resolve('./atlas.db'))
const db = new sqlite3.Database(path.resolve('./atlas.db'))

const insertReading = (type, reading) => {
  db.run(`INSERT INTO ${type} VALUES (datetime('now'), ${reading});`)
}

const fetchLatestReadings = (type, limit, callback) => {
  db.all(`SELECT * FROM ${type} ORDER BY createdAt DESC LIMIT ${limit}`, callback)
}

const fetchReading = (type, callback) => {
  db.get(`SELECT * FROM ${type};`, callback)
}

const fetchReadingsBetweenTime = (type, start, end, callback) => {
  db.all(`SELECT * FROM ${type} WHERE createdAt > ? AND createdAt < ? ORDER BY createdAt ASC;`, [start, end], callback)
}

const getAverageOfReadingsBetweenTime = (type, start, end, callback) => {
  db.get(`SELECT avg(value) FROM ${type} WHERE createdAt > ? AND createdAt < ?;`, [start, end], callback)
}

module.exports = {
  insertReading,
  fetchReading,
  fetchLatestReadings,
  fetchReadingsBetweenTime,
  getAverageOfReadingsBetweenTime
}
