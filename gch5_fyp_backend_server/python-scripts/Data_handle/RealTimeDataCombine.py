# This script is used to combine the real-time data from the drone and the station.
from datetime import datetime, timedelta
import json
import sys
import time
from shared_state import drone_data, station_data, combined_data

# save the data to json file
def save_message_to_json(message):
    with open('combined.json', 'a') as file:
        json.dump(message, file)
        file.write('\n')  # Add newline to separate messages
        
# Interpolate the location of the drone at the time of the station data
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
    interpolated_height = drone_before['height'] + (drone_after['height'] - drone_before['height']) * ratio
    return interpolated_lon, interpolated_lat, interpolated_height 

# This function is used to process COMBINED data
def process_combined_data(new_station_point):
    global drone_data, station_data
    for i in range(len(drone_data) - 1):
        if drone_data[i]['time'] <= new_station_point['time'] <= drone_data[i+1]['time']:
            inter_lon, inter_lat, inter_height = interpolate_location(drone_data[i], drone_data[i+1], new_station_point['time'])
            combined_data = {
                "type": "real_time_data",
                "data":{
                    'device_id': new_station_point['device_id'],
                    'time': new_station_point['time'],
                    'rssi': new_station_point['rssi'],
                    'lon': inter_lon,
                    'lat': inter_lat,
                    'height': inter_height                
                    }
            }
            # remove the past drone data
            drone_data = drone_data[i:]
            print(combined_data)
            save_message_to_json(combined_data)
            return combined_data
    
        
# this function is used to start combining data
def start_combining_data():
    global drone_data, station_data
    while True:
        if station_data:
            combined_data = process_combined_data(station_data[0])
            if combined_data:
                json_data = json.dumps(combined_data)
                print(json_data)
                sys.stdout.flush()
                station_data.pop(0)
            else:
                time.sleep(0.5)
        else:
            print("No station data received yet. Please wait for a moment.")
            time.sleep(0.5)
