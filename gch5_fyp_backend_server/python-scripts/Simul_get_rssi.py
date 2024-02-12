from scipy.interpolate import griddata
import numpy as np
import pandas as pd
import sys
import json
import threading
import time
import random
from datetime import datetime
from shared_state import current_drone_location, combined_data, initial_location
from Coordinate_transfer import xy2ll

df = pd.read_csv('./compiled_data.csv')

# Interpolate RSSI values for given x, y (this is a placeholder for your actual interpolation logic)
def interpolate_rssi(x, y, df):
    # Prepare data for interpolation
    points = df[['x', 'y']].values
    rssi_values = df['rssi'].values
    # Adjust state if necessary (based on the interpolation logic)
    if y < 0:
        y = -y
    # Perform cubic interpolation
    interpolated_rssi = griddata(points, rssi_values, ([x, y]), method='cubic')
    # Check if interpolation was successful; otherwise, use a fallback value or method
    if interpolated_rssi.size == 0 or np.isnan(interpolated_rssi):
        interpolated_rssi = -100
        print("ERROR To imterpolate rssi value")

    return interpolated_rssi[0]

# Continuous drone simulation and data combination
def rt_drone_simul_rssi_combine():
    global current_drone_location, combined_data

    while True:
        # Read the current drone location
        x, y = current_drone_location
        # Interpolate RSSI for the current location
        rssi = interpolate_rssi(x, y, df)

        entry = {
            'x': x,
            'y': y,
            'rssi': rssi
        }
        combined_data.append(entry)
        # Convert x, y to latitude and longitude
        lon, lat = xy2ll(x, y,initial_location[0], initial_location[1])
        # Create combined data entry
        time_now = datetime.now()
        combined_entry = {
            'type': 'real_time_data',
            'data': {
                'time': time_now.isoformat(),
                'lon' : lon,
                'lat' : lat,
                'rssi': rssi
            }
        }      

        # Emit combined_entry as JSON to frontend
        json_data = json.dumps(combined_entry)
        print(json_data)
        sys.stdout.flush()

        time.sleep(1)  # Simulate data generation every second

def background_drone_add_rssi():
    thread = threading.Thread(target=rt_drone_simul_rssi_combine)
    thread.start()

if __name__ == "__main__":
    background_drone_add_rssi()