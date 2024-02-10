// Import necessary modules
const express = require('express');
const cors = require('cors');
const { spawn } = require('child_process');

// Import routes
const droneNavigationRoutes = require('./routes/droneNavigation');
const excelDataRoutes = require('./routes/excelData');
const { setupRealTimeDataSSE } = require('./routes/RealTimeDataEmit');

// Initialize Express app
const app = express();
const port = 3000;

// Middleware setup
app.use(cors());
app.use(express.json());

// Routes setup
app.use('/drone-navigation', droneNavigationRoutes);
app.use('/get-excel-data', excelDataRoutes);

// Set up SSE endpoint for real-time data
setupRealTimeDataSSE(app);

// Default route
app.get('/', (req, res) => {
  res.send('Node.js server is running');
});



await generateExecutionId();
const executionId = getExecutionId();

// Start the Python script with the executionId
const pythonProcess = spawn('python', ['./python-scripts/Testing.py', executionId]);

pythonProcess.stdout.on('data', (data) => {
    console.log(`Python script output: ${data}`);
});

pythonProcess.stderr.on('data', (data) => {
    console.error(`Python script error: ${data}`);
});

// Start the server
app.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    });

