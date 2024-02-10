const { spawn } = require('child_process');
const dataEmitter = require('../events/DataEmitter');

const runPythonScript = (scriptPath, eventName) => {
  const pythonProcess = spawn('python', [scriptPath]);

  pythonProcess.stdout.on('data', (data) => {
    const result = data.toString();
    // Emitting data with a specific event name
    dataEmitter.emit(eventName, result);
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`stderr: ${data}`);
  });
};

module.exports = { runPythonScript };