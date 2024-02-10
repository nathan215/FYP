const express = require('express');
const router = express.Router();
const dataEmitter = require('../events/DataEmitter');

router.get('/', function(req, res) {
  req.setTimeout(Number.MAX_VALUE);

  res.writeHead(200, {
    'Content-Type': 'text/event-stream',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
  });

  const sendData = (data,event) => {
    res.write(`event: ${event}\n`);
    res.write(`data: ${JSON.stringify(data)}\n\n`);
  };

  const newDataListener = (data) => {
    sendData(data, 'DroneNavigation');
  }
  
  dataEmitter.on('newData', newDataListener);

  req.on('close', () => {
    dataEmitter.removeListener('newData', newDataListener);
  });
});

module.exports = router;