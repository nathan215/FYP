from datetime import datetime, timedelta
import requests
import json

# Example data structures
drone_data = [
    {'time': datetime.now() - timedelta(minutes=2), 'lat': 40.7128, 'lon': -74.0060},
    {'time': datetime.now(), 'lat': 40.7138, 'lon': -74.0070}
]
station_data = [
    {'time': datetime.now() - timedelta(minutes=1), 'rssi': -70}
]

def interpolate_location(drone_before, drone_after, station_time):
    total_time_delta = (drone_after['time'] - drone_before['time']).total_seconds()
    elapsed_time = (station_time - drone_before['time']).total_seconds()
    
    if total_time_delta == 0:
        return drone_before['lat'], drone_before['lon']
    
    ratio = elapsed_time / total_time_delta
    interpolated_lat = drone_before['lat'] + (drone_after['lat'] - drone_before['lat']) * ratio
    interpolated_lon = drone_before['lon'] + (drone_after['lon'] - drone_before['lon']) * ratio
    
    return interpolated_lat, interpolated_lon

def process_new_station_data(new_station_point):
    for i in range(len(drone_data) - 1):
        if drone_data[i]['time'] <= new_station_point['time'] <= drone_data[i+1]['time']:
            interpolated_lat, interpolated_lon = interpolate_location(drone_data[i], drone_data[i+1], new_station_point['time'])
            combined_data = {
                'time': new_station_point['time'],
                'lat': interpolated_lat,
                'lon': interpolated_lon,
                'rssi': new_station_point['rssi']
            }
            
            # Actions to take with the combined data
            print_to_frontend(combined_data) 
            return

def print_to_frontend(data):
    url = 'http://localhost:3000/data'
    response = requests.post(url, json=data)
    print('Response from Node.js:', response.text)


# Example usage
new_station_point = {'time': datetime.now() - timedelta(minutes=1, seconds=30), 'rssi': -75}
process_new_station_data(new_station_point)
