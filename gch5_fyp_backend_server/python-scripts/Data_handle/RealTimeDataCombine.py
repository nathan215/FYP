from datetime import datetime, timedelta
import json
import sys
import time
from shared_state import drone_data, station_data, find_device_id, fix_device_id,\
    find_combined_data, fix_combined_data, find_initial_location, fix_initial_location
import threading
from Data_handle.Coordinate_transfer import ll2xy
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(dir_path, '..', '..', 'combined.json')

# Save the data to json file
def save_message_to_json(message):
    with open(file_path, "a") as file:
        json.dump(message, file)
        file.write("\n")  # Add newline to separate messages

# Interpolate the location of the drone at the time of the station data
def interpolate_location(drone_before, drone_after, station_time_str):
    # Convert ISO format strings back to datetime objects
    drone_before_time = datetime.fromisoformat(drone_before["time"])
    drone_after_time = datetime.fromisoformat(drone_after["time"])
    station_time = datetime.fromisoformat(station_time_str)

    total_time_delta = (drone_after_time - drone_before_time).total_seconds()
    elapsed_time = (station_time - drone_before_time).total_seconds()

    if total_time_delta == 0:
        return drone_before["lat"], drone_before["lon"], drone_before.get("height", 0)

    ratio = elapsed_time / total_time_delta
    interpolated_lat = (
        drone_before["lat"] + (drone_after["lat"] - drone_before["lat"]) * ratio
    )
    interpolated_lon = (
        drone_before["lon"] + (drone_after["lon"] - drone_before["lon"]) * ratio
    )
    interpolated_height = (
        drone_before.get("height", 0)
        + (drone_after.get("height", 0) - drone_before.get("height", 0)) * ratio
    )
    return interpolated_lon, interpolated_lat, interpolated_height

# This function is used to process COMBINED data
def process_combined_data(new_station_point, websocket_server):
    for i in range(len(drone_data) - 1):
        if (
            drone_data[i]["time"]
            <= new_station_point["time"]
            <= drone_data[i + 1]["time"]
        ):
            inter_lon, inter_lat, inter_height = interpolate_location(
                drone_data[i], drone_data[i + 1], new_station_point["time"]
            )

            combine_data = {
                "type": "real_time_data",
                "data": {
                    "device_id": new_station_point["device_id"],
                    "time": new_station_point["time"],
                    "rssi": new_station_point["rssi"],
                    "lon": inter_lon,
                    "lat": inter_lat,
                    "height": inter_height
                },
            }

            if find_device_id  and  find_device_id[0] == new_station_point["device_id"]:
                x, y = ll2xy(inter_lon, inter_lat, find_initial_location[0], find_initial_location[1])
                entry = {
                    "x": x,
                    "y": y,
                    "rssi": new_station_point["rssi"]
                }
                find_combined_data.append(entry)

            if fix_device_id and fix_device_id[0] == new_station_point["device_id"]:
                x, y = ll2xy(inter_lon, inter_lat, fix_initial_location[0], fix_initial_location[1])
                entry = {
                    "x": x,
                    "y": y,
                    "rssi": new_station_point["rssi"]
                }

            save_message_to_json(combine_data)  # Optionally save to file
            websocket_server.send_message(combine_data)
            
            # delete previous drone data before i
            for k in range(i):
                drone_data.pop(0)

            return combine_data
    return None

# This function is used to start combining data
def start_combining_data_once(websocket_server):
    while True:
        if station_data:
            combined_data = process_combined_data(station_data[0], websocket_server)
            if combined_data:
                station_data.pop(0)
            else:
                if station_data[0]['time'] < drone_data[0]['time']:
                    station_data.pop(0)
                print("No drone data to combine with station data")
                time.sleep(0.5)
        else:
            if len(drone_data) > 10:
                drone_data.pop(0)
            time.sleep(0.5)

def start_combining_data(websocket_server):
    print("Starting data combining...")
    thread = threading.Thread(
        target=start_combining_data_once, args=(websocket_server,)
    )
    thread.start()
