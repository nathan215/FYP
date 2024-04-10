const WebSocket = require('ws');

const ws = new WebSocket('ws://127.0.0.1:9001');

ws.onmessage = function(event) {
  const message = JSON.parse(event.data);
  switch(message.type) {
    case "real_time_data":
      console.log("Received real-time data:", message.data);
      break;
    case "predict_location":
      console.log("Predicted location:", message.data);
      break;
    default:
      console.error("Unknown message type:", message.type);
  }
};