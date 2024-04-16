# This file is used to run the algorithm and send the next location of droneto frontend
import time
import numpy as np
import json
import sys
from .Drone_Control import fly_to_point
from Algorithm.path_loss_algorithm import compute_parameters_linear
from Algorithm.l3m_navigation import move_towards_l3m
from Algorithm.nelder_mead import my_nelder_mead
from Algorithm.nelder_mead_global import my_nelder_mead as my_nelder_mead_global
from shared_state import find_device_id, fix_device_id, find_initial_location, fix_initial_location, \
find_combined_data, fix_combined_data, current_drone_location, algorithm_use , Z0, alpha
from Data_handle.Coordinate_transfer import xy2ll
from .path_draw import draw_path
import threading
# This function is used to receive the rssi value of the drone
def rssi_receive(x, websocket_server):
    
    lon, lat = xy2ll(x[0], x[1], find_initial_location[0], find_initial_location[1])
    x_re = {"type": "predict_location", "data": {"lon": lon, "lat": lat}}
    print(f"Sending predicted location: {x_re}")
    websocket_server.send_message(x_re)
    draw_path()
    rssi = None
    fly_to_point(x)
    

    time.sleep(0.5)
    while True:
        if np.linalg.norm(np.array(current_drone_location) - np.array(x)) <= 0.01:
            for data in find_combined_data:
                drone_location = np.array([data["x"], data["y"]])
                if np.linalg.norm(drone_location - np.array(x)) <= 0.01:
                    rssi = data["rssi"]
            if rssi is not None:
                print(f"Received RSSI: {rssi} at {x}")
                return -rssi
            else:
                print(
                    "RSSI data not found for the current location. Waiting..."
                )
                time.sleep(0.5)

def caculate_parameter():
    global fix_combined_data, ZO, alpha
    while True:
        print("Use the path loss parameters by the device")
        if len(fix_combined_data) < 3:
            print("The number of data points is less than 3, use the default path loss parameters")
            Z0, alpha = -40,2
        else:
            Z0, alpha,error = compute_parameters_linear(fix_combined_data)
            print("The path loss parameters are: ",Z0,alpha,error)
        time.sleep(4)


# This function is used to run the algorithm
def run_algorithm(websocket_server):
    global current_drone_location, algorithm_use, find_combined_data, fix_combined_data
    # clean find_combined_data and fix_combined_data
    find_combined_data.clear()
    fix_combined_data.clear()
        
    current_drone_location_array = np.array(current_drone_location)
    if algorithm_use[0] == "nelder_mead":
        print("start nelder_mead algorithm")
        minimum, points_evaluated = my_nelder_mead(
            lambda x: rssi_receive(x, websocket_server), current_drone_location_array
        )
    elif algorithm_use[0] == "nelder_mead_global":
        print("start nelder_mead_global algorithm")
        minimum, points_evaluated = my_nelder_mead_global(
            lambda x: rssi_receive(x, websocket_server),
            current_drone_location_array,
        )
    elif algorithm_use[0] == "l3m":

        print("Please randomly move the drone to collect data for the algorithm")
        x,y = current_drone_location
        fly_to_point([x+100,y])
        fly_to_point([x+100,y+100])
        if find_device_id:
            thread = threading.Thread(target=caculate_parameter)
            thread.start()
        print("start l3m algorithm")
        minimum, points_evaluated = move_towards_l3m(
            lambda x: rssi_receive(x, websocket_server),
            current_drone_location_array,
            all_points= find_combined_data,
        )


if __name__ == "__main__":
    run_algorithm()
