# Backend Server Overview

The backend server is designed to handle data received from drones and various sources (e.g., TTN), process this data through algorithms, and transmit the results. It supports operations in two modes: data collection and simulation for algorithm testing.

## Directory Structure

/backend_server
│
├── python_script/
│ ├── Algorithm/
│ │ ├── l3m_navigation.py # Drone navigation using path loss function localization
│ │ └── nelder_mead.py # Standard Nelder-Mead optimization
│ │ └── nelder_mead_global.py # Enhanced Nelder-Mead avoiding local maxima
│ ├── Data_handle/
│ │ ├── Coordinate_transfer.py # Converts lat/lon to Cartesian coordinates (x, y)
│ │ ├── RealTimeDataCombine.py # Combines drone and station data via interpolation
│ │ └── DataGenerate.py # Generates simulation data
│ │ └── Simul_get_rssi.py # Retrieves RSSI data for simulations
│ ├── Data_transmission/
│ │ ├── MQTT_Drone.py # Interfaces with DJI Pilot2 API via MQTT
│ │ ├── MQTT_Station.py # Receives data from TTN via MQTT
│ │ └── websocket_server.py # Manages websocket connections for data transmission
│ ├── Process/
│ │ ├── Algorithm_run.py # Manages algorithm execution
│ │ └── Drone_Control.py # Controls drone during simulations
│ ├── Main.py # Main script to start the backend server
│ └── shared_state.py # Manages shared state across modules
│
├── src/ # Currently unused
├── Testing_Html/ # HTML files for testing
└── (data folders and results) # Directories for storing data and results

## Installation and Execution

1. **Installation**: Ensure all necessary libraries are installed as specified in the requirements file.
2. **Running the Server**: Execute `Main.py` to start the server. The server operates in two modes:
   - `Data`: For real-time data collection.
   - `Simulation`: For testing algorithms with simulation datasets.

## Modules Description

- **Algorithm**: Contains algorithms for navigation and optimization, including path loss-based localization and Nelder-Mead optimization techniques.
- **Data Handle**: Manages data transformations and combinations, useful for processing incoming data and preparing it for algorithms.
- **Data Transmission**: Handles the communication between the server and external devices (drones and stations) through MQTT, and facilitates data flow to the frontend via websockets.
- **Process**: Orchestrates the running of algorithms and the control of simulation en