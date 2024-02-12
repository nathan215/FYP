from datetime import datetime, timedelta
import json
import sys
import time
from shared_state import drone_data, station_data, combined_data

def interpolate_location(drone_before, drone_after, station_time_str):
    # Convert ISO format strings back to datetime objects
    drone_before_time = datetime.fromisoformat(drone_before['time'])
    drone_after_time = datetime.fromisoformat(drone_after['time'])
    station_time = datetime.fromisoformat(station_time_str)
    
    total_time_delta = (drone_after_time - drone_before_time).total_seconds()
    elapsed_time = (station_time - drone_before_time).total_seconds()
    
    if total_time_delta == 0:
        return drone_before['lat'], drone_before['lon']
    
    ratio = elapsed_time / total_time_delta
    interpolated_lat = drone_before['lat'] + (drone_after['lat'] - drone_before['lat']) * ratio
    interpolated_lon = drone_before['lon'] + (drone_after['lon'] - drone_before['lon']) * ratio
    
    return interpolated_lon, interpolated_lat

def process_new_station_data(new_station_point):
    global drone_data, station_data
    for i in range(len(drone_data) - 1):
        if drone_data[i]['time'] <= new_station_point['time'] <= drone_data[i+1]['time']:
            interpolated_lon, interpolated_lat = interpolate_location(drone_data[i], drone_data[i+1], new_station_point['time'])
            combined_data = {
                "type": "real_time_data",
                "data":{
                    'time': new_station_point['time'],
                    'lon': interpolated_lon,
                    'lat': interpolated_lat,                
                    'rssi': new_station_point['rssi']}
            }
            return combined_data

def start_combining_data():
    global drone_data, station_data
    while True:
        if station_data:
            combined_data = process_new_station_data(station_data[0])
            if combined_data:
                json_data = json.dumps(combined_data)
                print(json_data)
                sys.stdout.flush()
                station_data.pop(0)
            else:
                time.sleep(0.5)
        time.sleep(0.5)

# def data_return():
#     global combined_data, current_location
#     while True:
#         if current_location:
            