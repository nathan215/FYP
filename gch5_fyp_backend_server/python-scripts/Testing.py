import random
from datetime import datetime, timedelta
import threading
import time
from shared_state import drone_data, station_data

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


def start_generating_data():
    drone_thread = threading.Thread(target=generate_drone_data)
    station_thread = threading.Thread(target=generate_station_data)

    drone_thread.start()
    station_thread.start()

