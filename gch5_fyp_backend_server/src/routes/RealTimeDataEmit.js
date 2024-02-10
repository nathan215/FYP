const { getExecutionId } = require('../services/executionIdManager');
const { MongoClient } = require('mongodb');
const { EventEmitter } = require('events');
const dataEmitter = new EventEmitter();

// Initialize MongoDB Client 
const mongoClient = new MongoClient('mongodb://127.0.0.1:27017');

const dbName = 'FYP';
const collectionName = 'RealTimeData';

// Set up the server-sent events endpoint
const setupRealTimeDataSSE = (app) => {
    app.get('/real-time-data', async (req, res) => {
        const currentExecutionId = getExecutionId();

        res.setHeader('Content-Type', 'text/event-stream');
        res.setHeader('Cache-Control', 'no-cache');
        res.setHeader('Connection', 'keep-alive');

        try {
            await mongoClient.connect();
            console.log('Connected to MongoDB for SSE');

            const db = mongoClient.db(dbName);
            const collection = db.collection(collectionName);

            // Start listening to change stream for the collection
            const changeStream = collection.watch([
                { $match: { 'fullDocument.execution_id': currentExecutionId } }
            ]);

            changeStream.on('change', (change) => {
                console.log('Change detected:', change);
                // Send the full document of the change to the client
                res.write(`data: ${JSON.stringify(change.fullDocument)}\n\n`);
            });

            // Cleanup on client disconnect
            req.on('close', () => {
                console.log('Client disconnected, closing change stream');
                changeStream.close();
                res.end();
            });
        } catch (error) {
            console.error('Error connecting to MongoDB:', error);
            res.status(500).send('Failed to connect to MongoDB');
        }
    });
};

module.exports = { setupRealTimeDataSSE };
