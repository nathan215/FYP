const EventEmitter = require('events');
class DataEmitter extends EventEmitter {}
module.exports = new DataEmitter();
