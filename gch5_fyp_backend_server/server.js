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
// Function to start and manage SeperateJob.py
function startPython() {
    console.log('Starting SeperateJob.py');
    const pythonProcess = spawn('python', ['./python-scripts/SeperateJob.py']);

    pythonProcess.stdout.on('data', (data) => {
        const message = data.toString().trim();
        console.log(message);
        try {
            const jsonData = JSON.parse(message);
            // Depending on the type of data, emit to different events
            switch (jsonData.type) {
                case 'real_time_data':
                    io.emit('realtime_data_update', jsonData.data);
                    break;
                case 'predict_location':
                    io.emit('predict_location_update', jsonData.data);
                    break;
                case 'drone_navigation':
                    io.emit('drone_navigation_update', jsonData.data);
                    break;
                default:
                    console.error('Unrecognized data type from Python script:', jsonData.type);
            }
        } catch (error) {
            console.error('Error parsing JSON from Python script:', error);
        }
    });

    pythonProcess.stderr.on('data', (data) => {
        console.error(`Python script error: ${data}`);
    });

    // Handle Python process exit
    pythonProcess.on('close', (code) => {
        console.log(`SeperateJob.py process exited with code ${code}`);
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