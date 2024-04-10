# This file is used to run the algorithm and send the next location of droneto frontend
import time
import numpy as np
import json
import sys
from .Drone_Control import fly_to_point
from Algorithm.my_nelder_mead import my_nelder_mead
from shared_state import initial_location, combined_data, current_drone_location
from Data_handle.Coordinate_transfer import xy2ll


# This function is used to receive the rssi value of the drone
def rssi_receive(x, websocket_server):
    rssi = None
    fly_to_point(x)
    # turn x to json
    lon, lat = xy2ll(x[0], x[1], initial_location[0], initial_location[1])
    x_re = {"type": "drone_navigation", "data": {"lon": lon, "lat": lat}}
    # next_place = json.dumps(x_re)
    # print(next_place)
    websocket_server.send_message(x_re)
    time.sleep(0.5)
    while True:
        if np.linalg.norm(np.array(current_drone_location) - np.array(x)) <= 0.01:
            for data in combined_data:
                drone_location = np.array([data["x"], data["y"]])
                if np.linalg.norm(drone_location - np.array(x)) <= 0.01:
                    rssi = data["rssi"]
            if rssi is not None:
                print(f"Received RSSI: {rssi} at {x}")
                return -rssi
            else:
                print(
                    "RSSI data not found for the current location. Please check combined_data."
                )
                time.sleep(0.5)


# This function is used to run the algorithm
def run_algorithm(websocket_server):
    global current_drone_location
    print("start")
    current_drone_location_array = np.array(current_drone_location)
    minimum, points_evaluated = my_nelder_mead(
        lambda x: rssi_receive(x, websocket_server), current_drone_location_array
    )


if __name__ == "__main__":
    run_algorithm()
