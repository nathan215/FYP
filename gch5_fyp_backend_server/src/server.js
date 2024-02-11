const express = require('express');
const { spawn } = require('child_process');
const http = require('http');
const { Server } = require("socket.io");
const { start } = require('repl');

const app = express();
const server = http.createServer(app);
const io = new Server(server, {
    cors: {
        origin: "*", // Allow all origins
        methods: ["GET", "POST"], // Allow only GET and POST requests
    }
});
const port = 3000;

app.use(express.json());

// Setup WebSocket communication
io.on('connection', (socket) => {
    console.log('A client connected');
    socket.on('disconnect', () => console.log('Client disconnected'));
});

// Function to start and manage SeperateJob.py
function startPython() {
    console.log('Starting SeperateJob.py');
    const pythonProcess = spawn('python', ['./python-scripts/SeperateJob.py']);

    pythonProcess.stdout.on('data', (data) => {
        const message = data.toString().trim();
        try {
            const jsonData = JSON.parse(message);
            // Push data to all connected clients
            io.emit('realtime_data', jsonData);
        } catch (error) {
            console.error('Error parsing JSON from Python script:', message);
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python script error: ${data}`);
    });

    // Handle Python process exit
    pythonProcess.on('close', (code) => {
        console.log(`RealTimeDataCombine.py process exited with code ${code}`);
        // Consider restarting the Python process if it exits unexpectedly
    });
}

// Function to start Testing.py
function startTesting() {
    const pythonProcess = spawn('python', ['./python-scripts/Testing.py']);
}

// Start the server and the continuous Python script
server.listen(port, () => {
    console.log(`Server listening at http://localhost:${port}`);
    startPython();
});

// Example route to handle other requests
app.get('/status', (req, res) => {
    res.json({ status: 'Server is running and processing data' });
});

// Define a route for the root path
app.get('/', (req, res) => {
    res.send('Server is running');
});