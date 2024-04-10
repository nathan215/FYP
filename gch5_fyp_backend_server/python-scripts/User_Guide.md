# WebSocket Service User Guide

This guide provides essential information on how to use the WebSocket service for real-time data transmission, including drone positions and signal strength (RSSI), and sending drone destination predictions.

## 1. WebSocket Connection

To establish a WebSocket connection, connect to the provided WebSocket URL. This service allows for real-time communication between the server and clients.

## 2. Example Usage Code

Find example usage code in the `Testing_Html` folder, which demonstrates how to utilize the WebSocket service in html, python and java

## 3. Data Types

### Data Format
Data is transmitted in JSON format, with two primary message types:

#### 1. Drone Position and RSSI (`real_time_data`)
```json
{
  "type": "real_time_data",
  "data": {
    "device_id": "device123",
    "time": "2024-04-01T12:00:00Z",
    "rssi": -70,
    "lon": 34.052235,
    "lat": -118.243683,
    "height": 100
  }
}
```

#### 2. Drone Next Destination (predict_location)

```json
{
  "type": "predict_location",
  "data": {
    "lon": 34.052235,
    "lat": -118.243683
  }
}
```

## 4. How to Start the Server

To start the WebSocket server:

    Run Main.py: Execute Main.py directly. This script initializes the WebSocket server and starts listening for incoming connections.

    bash


WebSocket Settings: Configuration for the WebSocket server, including port and connection settings, is located in the Data_transmission folder.