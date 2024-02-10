// In ./db/index.js
const { MongoClient } = require('mongodb');

const uri = "mongodb://127.0.0.1:27017";
const dbName = "FYP";

const client = new MongoClient(uri);

const connectDB = async () => {
    try {
        await client.connect();
        console.log("Connected to MongoDB");
        const db = client.db(dbName);
        return db; 
    } catch (error) {
        console.error("Could not connect to MongoDB", error);
        process.exit(1);
    }
};

module.exports = connectDB;
