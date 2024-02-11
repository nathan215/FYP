import random
from datetime import datetime, timedelta
import threading
import time
from shared_state import drone_data, station_data
import pandas as pd
import math


R = 6371000  # Radius of the Earth in meters
start_lat = 22.337
start_lon = 114.268

def generate_drone_data():
    global drone_data
    while True:
        time_now = datetime.now()
        new_drone_data = {
            'time': time_now.isoformat(),
            'lat': round(random.uniform(22.3370, 22.3360), 6),
            'lon': round(random.uniform(114.2635,114.2645), 6)
        }
        drone_data.append(new_drone_data)
        time.sleep(1)  # Generate new drone data every second

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

def xy2ll(x, y, start_lat=start_lat, start_lon=start_lon):
    # Convert back to latitude and longitude
    start_lat_rad = math.radians(start_lat)
    lat = y / R + start_lat
    lon = x / (R * math.cos(start_lat_rad)) + start_lon
    
    return lat, lon

# Load data
df = pd.read_csv('./compiled_data.csv')
# random the index
df = df.sample(frac=1).reset_index(drop=True)
# change x, y to lat, lon
for index, row in df.iterrows():
    df.at[index, 'lat'], df.at[index, 'lon'] = xy2ll(row['x'], row['y'])
# Shared index to keep track of current row for drone and station data
current_index = 0

def read_drone_data():
    global current_index
    global drone_data
    while current_index < len(df):
        row = df.iloc[current_index]
        # Assuming the CSV has 'lat' and 'lon' columns for drone data
        new_drone_data = {
            'time': datetime.now().isoformat(),  # Simulate real-time emission
            'lat': row['lat'],
            'lon': row['lon']
        }
        drone_data.append(new_drone_data)
        current_index += 1
        time.sleep(1)  # Wait for 1 second before the next drone data emission


def read_station_data():
    global current_index
    global station_data
    while  current_index< len(df):
        row = df.iloc[current_index]
        # Assuming the CSV has an 'rssi' column for station data
        new_station_data = {
            'time': datetime.now().isoformat(),  # Simulate real-time emission
            'rssi': row['rssi']
        }
        station_data.append(new_station_data)
        time.sleep(2)  # Wait for 2 seconds before checking again

# Start threads
def start_generating_data():
    drone_thread = threading.Thread(target=read_drone_data)
    station_thread = threading.Thread(target=read_station_data)

    drone_thread.start()
    station_thread.start()

