# this file is used to simulate the rssi value of the drone,and then send the rssi value 
from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import sys
import json
import threading
import time
from datetime import datetime
from shared_state import current_drone_location,data_path, \
find_combined_data, fix_combined_data, find_initial_location, fix_initial_location, device_id
from .Coordinate_transfer import xy2ll
from .RealTimeDataCombine import save_message_to_json
import os
dir_path = os.path.dirname(os.path.realpath(__file__))

file_path = os.path.join(dir_path, '..', '..', data_path)
df = pd.read_csv(file_path)

# Interpolate RSSI values for given x, y (this is a placeholder for your actual interpolation logic)
def interpolate_rssi(x, y, df):
    # Prepare data for interpolation
    points = df[['x', 'y']].values
    rssi_values = df['rssi'].values
    # Adjust state if necessary (based on the interpolation logic)
    if y < 0 and data_path == 'compiled_data.csv':
        y = -y
        interpolated_rssi = griddata(points, rssi_values, ([x, y]), method='cubic')
        # Check if interpolation was successful; otherwise, use a fallback value or method
        if interpolated_rssi.size == 0 or np.isnan(interpolated_rssi):
            interpolated_rssi = -100
            print("ERROR To imterpolate rssi value")
        return interpolated_rssi[0]
    else:
        x1,x2 = int(x),int(x)+1
        y1,y2 = int(y),int(y)+1
        # average of 4 points
        interpolated_rssi = (df[(df['x'] == x1) & (df['y'] == y1)]['rssi'].values[0] + df[(df['x'] == x1) & (df['y'] == y2)]['rssi'].values[0] + df[(df['x'] == x2) & (df['y'] == y1)]['rssi'].values[0] + df[(df['x'] == x2) & (df['y'] == y2)]['rssi'].values[0])/4
        return interpolated_rssi
    
# Continuous drone simulation and data combination
def rt_drone_simul_rssi_combine(websocket_server):
    global current_drone_location, find_combined_data, fix_combined_data, device_id
    device_id.append('testing_1')
    device_id.append('fixing_1')
    while True:
        # Read the current drone location
        x, y = current_drone_location[0], current_drone_location[1]
        # Interpolate RSSI for the current location
        rssi = interpolate_rssi(x, y, df)
        rssi_2 = rssi + np.random.normal(0,3)

        entry = {
            'x': x,
            'y': y,
            'rssi': rssi
        }
        find_combined_data.append(entry)

        entry_for_fix_device_id = {
            'x': x,
            'y': y,
            'rssi': rssi_2
        }
        fix_combined_data.append(entry_for_fix_device_id)
        # Convert x, y to latitude and longitude
        lon, lat = xy2ll(x, y,find_initial_location[0], find_initial_location[1])

        time_now = datetime.now()
        combined_entry = {
            'type': 'real_time_data',
            'data': {
                'device_id': 'testing_1',
                'time': time_now.isoformat(),
                'rssi': rssi,
                'lon' : lon,
                'lat' : lat,
                "height": 30
            }
        }
        fix_combine_entry = {
            'type': 'real_time_data',
            'data': {
                'device_id': 'fixing_1',
                'time': time_now.isoformat(),
                'rssi': rssi_2,
                'lon' : lon,
                'lat' : lat,
                "height": 30
            }
        }

        websocket_server.send_message(combined_entry)
        websocket_server.send_message(fix_combine_entry)
        # print("Combined data sent:", combined_entry)
        time.sleep(1)  # Simulate data generation every second

# Start the background thread for simulating drone data and combining it with station data
def background_drone_add_rssi(websocket_server):
    thread = threading.Thread(target=rt_drone_simul_rssi_combine(websocket_server))
    thread.start()

if __name__ == "__main__":
    background_drone_add_rssi()