# This script is used to generate SIMULATION drone and station data for testing purposes
import random
from datetime import datetime, timedelta
import threading
import time
import pandas as pd
from shared_state import drone_data, station_data, find_initial_location, find_device_id, fix_device_id
from .Coordinate_transfer import xy2ll
import os
# Get the directory of the current script
dir_path = os.path.dirname(os.path.realpath(__file__))

R = 6371000  # Radius of the Earth in meters
start_lat = 22.337
start_lon = 114.268

# Generate SIMULATION data
def generate_drone_data():
    global drone_data
    while True:
        time_now = datetime.now()
        new_drone_data = {
            'time': time_now.isoformat(),
            'lat': round(random.uniform(22.3370, 22.3360), 6),
            'lon': round(random.uniform(114.2635,114.2645), 6),
            'height': random.randint(0, 100),
        }
        drone_data.append(new_drone_data)
        time.sleep(1)  # Generate new drone data every second

# Generate SIMULATION data
def generate_station_data():
    global station_data
    while True:
        time_now = datetime.now()
        new_station_data = {
            'time': time_now.isoformat(),
            'rssi': random.randint(-100, 0)
        }
        station_data.append(new_station_data)
        time.sleep(2.5)  # Generate new station data every 2.5 seconds

# def start_generating_data():
#     drone_thread = threading.Thread(target=generate_drone_data)
#     station_thread = threading.Thread(target=generate_station_data)

#     drone_thread.start()
#     station_thread.start()

# Load data
# Construct the path to the file relative to the script location


file_path = os.path.join(dir_path, '..', '..', 'compiled_data.csv')
df = pd.read_csv(file_path)
# random the index
df = df.sample(frac=1).reset_index(drop=True)
# change x, y to lat, lon
for index, row in df.iterrows():
    df.at[index, 'lat'], df.at[index, 'lon'] = xy2ll(row['x'], row['y'],
                                    start_lat= find_initial_location[0],
                                    start_lon= find_initial_location[1])

current_index = 0

# Read data from the CSV file
def read_drone_data():
    global current_index
    global drone_data
    while current_index < len(df):
        row = df.iloc[current_index]
        # Assuming the CSV has 'lat' and 'lon' columns for drone data
        new_drone_data = {
            'time': datetime.now().isoformat(),  # Simulate real-time emission
            'lat': row['lat'],
            'lon': row['lon'],
            'height': random.randint(50, 51)
        }
        drone_data.append(new_drone_data)
        current_index += 1
        time.sleep(1)  # Wait for 1 second before the next drone data emission

# Read data from the CSV file
def read_station_data():
    global current_index
    global station_data
    while  current_index< len(df):
        row = df.iloc[current_index]
        # Assuming the CSV has an 'rssi' column for station data
        new_station_data = {
            'time': datetime.now().isoformat(),  # Simulate real-time emission
            'rssi': row['rssi'],
            'device_id': 'testing_1'
        }
        station_data.append(new_station_data)
        time.sleep(2)  # Wait for 2 seconds before checking again

# Generate SIMULATION data
def start_generating_data():
    print("Starting data generation...")
    drone_thread = threading.Thread(target=read_drone_data)
    station_thread = threading.Thread(target=read_station_data)
    drone_thread.start()
    station_thread.start()

